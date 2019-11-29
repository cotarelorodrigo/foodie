from sqlalchemy.orm.exc import NoResultFound
from src.auth.auth_exception import NotFoundException, NotEnoughFavourPoints
from src.auth.services.service import Service
from src.auth.services.shop_service import ShopService
import datetime
from dateutil import relativedelta

class OrderService(Service):
    def create_order(self, order_data):
        from src.auth.models.order_table import OrderModel, OrderProductsModel
        from src.auth.schemas.schemas import OrderSchema
        from src.auth.services.user_service import UserService
        order_schema = OrderSchema()
        order_info, products_info = order_schema.load(order_data)
        # if order_info["payWithPoints"]:
        #     user_service = UserService()
        #     if not user_service.user_order_by_favour(int(order_info["user_id"]), int(order_info["favourPoints"])):
        #         raise NotEnoughFavourPoints("Favour points insuficientes")
        order = OrderModel(order_info)
        products = [OrderProductsModel(product) for product in products_info]
        order.save() #Hay que guardar primero la orden orden porq es la parte unaria de la relacion
        for p in products:
            order.products.append(p)
            p.save()
        self.order_created(order.order_id)
        return order

    def get_orders(self):
        from src.auth.models.order_table import OrderModel
        response = OrderModel.query.all()
        if not response:
            return []
        return self.sqlachemy_to_dict(response)
    
    def get_order_by_id(self, _order_id):
        from src.auth.models.order_table import OrderModel
        order = OrderModel.query.filter_by(order_id=_order_id).one()
        return self.sqlachemy_to_dict(order)


    def calculate_price(self,_products_info):
        from src.auth.models.product_table import ProductModel
        price = 0.0
        for item in _products_info:
            product = ProductModel.query.get(item['product_id'])
            price += product['price'] * item['units']
            print("Price is " + price)
        return price

    def get_products_orders(self):
        from src.auth.models.order_table import OrderProductsModel
        response = OrderProductsModel.query.all()
        if not response:
            return []
        return self.sqlachemy_to_dict(response)

    def get_order_items(self,_order_id):
        from src.auth.models.order_table import OrderProductsModel
        response = OrderProductsModel.query.filter_by(order_id=_order_id)
        return self.sqlachemy_to_dict(response)

    ##Order states {'delivered', 'onWay', 'cancelled', 'created'}
    #State: On way
    def catch_order(self, _order_id, _delivery_id, offer_info):
        from src.app import db
        from src.auth.models.order_table import OrderModel
        from src.auth.services.user_service import UserService
        from src.auth.models.user_table import NormalUserModel, DeliveryUserModel
        order = OrderModel.get_instance(_order_id)
        user_service = UserService()
        if order.payWithPoints: #chequeo que el que acepto la orden sea un usuario normal, no delivery
            try:
                delivery_user = user_service.get_normal_user(_delivery_id)
                user = user_service.get_normal_user(order.user_id)
                user.favourPoints -= offer_info["points"]
                order.favourPoints = offer_info["points"]
            except:
                raise NotFoundException("ID invalido: Solo los usuarios comunes pueden aceptar favores")
        else:
            try:
                order.delivery_price = offer_info["delivery_price"]
                order.delivery_pay = offer_info["delivery_pay"]
                user_service.get_delivery_user(_delivery_id)
            except:
                raise NotFoundException("ID invalido: Delivery inexistente")  
        user_service.user_start_working(_delivery_id, _order_id)
        user_service.wait_order(order.user_id)
        order.delivery_id = _delivery_id
        self.change_order_state(_order_id, "onWay")
        order.save()
        return order

    #State: delivered
    def order_delivered(self, order_id):
        from src.auth.models.order_table import OrderModel
        from src.auth.services.user_service import UserService
        from src.auth.services.delivery_service import DeliveryService
        order = OrderModel.get_instance(order_id)
        order_info = {}
        user_service = UserService()
        del_service = DeliveryService()
        #Pagar al delivery
        if order.payWithPoints: #chequeo que el que acepto la orden sea un usuario normal, no delivery
            order_info["payWithPoints"] = True
            order_info['favourPoints'] = order.favourPoints
        else:
            order_info["payWithPoints"] = False
            order_info["delivery_price"] = order.delivery_price

        user_service.pay_order(order.user_id, order.delivery_id, order_info)
        user_service.user_finish_working(order.delivery_id)
        user_service.receive_order(order.user_id)
        self.change_order_state(order_id, "delivered")

    #State: cancelled
    def order_cancelled(self, order_id):
        self.change_order_state(order_id, "cancelled")

    #State: created
    def order_created(self, order_id):
        self.change_order_state(order_id, "created")

    def order_picked_up(self,order_id):
        self.change_order_state(order_id,"pickedUp")

    def change_order_state(self, _order_id, _state):
        from src.auth.models.order_table import OrderModel
        from src.auth.schemas.schemas import OrderState
        from src.auth.auth_exception import InvalidInformation
        order = OrderModel.query.filter_by(order_id=_order_id).one()
        if _state in OrderState:
            order.state = _state
            order.save()
        else:
            raise InvalidInformation('Estado de orden invalido')
        return order

    def get_quantity_complete_orders(self):
        from src.auth.models.order_table import OrderModel
        return OrderModel.query.filter_by(state='delivered').count()

    def get_quantity_cancelled_orders(self):
        from src.auth.models.order_table import OrderModel
        return OrderModel.query.filter_by(state='cancelled').count()

    def get_quantity_orders_date(self, date_from, date_to, state='delivered'):
        from src.auth.models.order_table import OrderModel
        return OrderModel.query.filter(OrderModel.state == state).filter(OrderModel.created_at >= date_from).filter(OrderModel.created_at <= date_to).count()

    def get_quantity_orders_by_month(self, year_from, month_from, year_to, month_to, state):
        date_from = datetime.date(year=year_from,month=month_from, day=1)
        date_to = datetime.date(year=year_to,month=month_to, day=1)
        result = []
        delta = relativedelta.relativedelta(date_from, date_to)
        for delta_month in range(abs(delta.months)):
            date_from_aux = date_from + relativedelta.relativedelta(months=delta_month)
            date_to_aux = date_from + relativedelta.relativedelta(months=delta_month+1)
            result.append({"year": date_to_aux.year, "month": date_to_aux.month, "amount": self.get_quantity_orders_date(date_from_aux, date_to_aux, state)})
        return result

    def get_today_delivery_orders(self, delivery_id):
        from src.auth.models.order_table import OrderModel
        from src.auth.models.user_table import DeliveryUserModel
        DeliveryUserModel.get_delivery(delivery_id)
        today = datetime.date.today()
        return OrderModel.query.filter(OrderModel.delivery_id == delivery_id).filter(OrderModel.created_at >= today).filter(OrderModel.state == 'delivered').count()

    def get_historical_user_orders(self, user_id):
        from src.auth.models.order_table import OrderModel
        from src.auth.models.user_table import NormalUserModel
        NormalUserModel.get_user(user_id)
        return OrderModel.query.filter(OrderModel.delivery_id == user_id).filter(OrderModel.state == 'delivered').count()

    def get_N_orders_filtered(self, pageNumber, pageSize, filters):
        from src.auth.models.order_table import OrderModel
        result = OrderModel.query.filter_by(**filters).offset(pageNumber*pageSize).limit(pageSize)
        response = {}
        response['items'] = self.sqlachemy_to_dict(result.all())
        response['totalItems'] = result.count()
        return response

    def review_shop(self,_order_id,review):
        from src.auth.models.order_table import OrderModel
        order = OrderModel.query.filter_by(order_id=_order_id).one()
        shop_service = ShopService()
        shop_id = order.shop_id
        shop_service.add_review(shop_id,review)
        order.shop_review = review
        order.save()
        return self.sqlachemy_to_dict(order)

    def review_delivery(self,_order_id,review):
        from src.auth.models.order_table import OrderModel
        from src.auth.services.delivery_service import DeliveryService

        order = OrderModel.query.filter_by(order_id=_order_id).one()
        del_service = DeliveryService()
        delivery_id = order.delivery_id
        del_service.add_review(delivery_id,review)
        order.delivery_review = review
        order.save()
        return self.sqlachemy_to_dict(order)