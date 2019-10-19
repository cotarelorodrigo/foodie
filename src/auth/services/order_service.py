from sqlalchemy.orm.exc import NoResultFound
from src.auth.auth_exception import NotFoundException
from src.auth.services.service import Service

class OrderService(Service):
    def create_order(self, order_data):
        from src.auth.models.order_table import OrderModel
        from src.auth.models.order_product_table import OrderProductsModel
        from src.auth.schemas.schemas import ProductSchema
        order_info = {
                "shop_id": order_data['shop_id'],
                "latitud": order_data['coordinates']['latitude'],
                "longitud": order_data['coordinates']['longitude'],
                "payWithPoints": order_data['payWithPoints']
        }
        order = OrderModel(order_info)
        products = []
        for product in order_data['products']:
            p = {"product_id": product['product_id'],
                "units": product['units']}
            #p = ProductSchema(p).load(p)
            products.append(OrderProductsModel(p))

        order.save() #Hay que guardar primero la orden orden porq es la parte unaria de la relacion
        for p in products:
            order.products.append(p)
            p.save()


    def get_orders(self):
        from src.auth.models.order_table import OrderModel
        response = OrderModel.query.all()
        if not response:
            return []
        return self.sqlachemy_to_dict(response)
    
    def get_products_orders(self):
        from src.auth.models.order_product_table import OrderProductsModel
        response = OrderProductsModel.query.all()
        if not response:
            return []
        return self.sqlachemy_to_dict(response)

    def delete_order(self,_id):
        from src.app import db
        from src.auth.models.order_table import OrderModel
        response = OrderModel.query.filter_by(order_id=_id).delete()
        db.session.commit()
        return response
