from marshmallow import Schema, fields, post_load, post_dump


class UserSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    phone_number = fields.Int(required=True)
    #role = fields.String(required=True)
    password = fields.Str(required=True)
    firebase_uid = fields.Str(required=True)

    class Meta:
        strict = True

class NormalUserSchema(UserSchema):
    role = fields.Str(required=True, validate=lambda s: s =='usuario')
    picture = fields.Str(required=False)
    suscripcion = fields.Str(required=True)

    class Meta:
        strict = True

class DeliveryUserSchema(UserSchema):
    role = fields.Str(required=True, validate=lambda s: s =='delivery')
    picture = fields.Str(required=True)
    balance = fields.Float(required=True)

    class Meta:
        strict = True

class CoordinateSchema(Schema):
    latitude = fields.Float(required=True)
    longitude = fields.Float(required=True)

    class Meta:
        strict = True

class ShopSchema(Schema):
    name = fields.Str(required=True)
    address = fields.Str(required=True)
    description = fields.Str(required=False)
    coordinates = fields.Nested(CoordinateSchema, required=True)
    photoUrl = fields.Str(required=True)
    rating = fields.Int(required=True)
    #To do: Falta meter el campo menu, que seria?

    @post_load
    def make_order_products(self, data, **kwargs):
        coordinates = data.pop('coordinates')
        data['latitude'] = coordinates['latitude']
        data['longitude'] = coordinates['longitude']
        return data

    class Meta:
        strict = True

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)

    class Meta:
        strict = True

class RecoverSchema(Schema):
    email = fields.Email(required=True)

    class Meta:
        strict = True

class OrderProductSchema(Schema):
    product_id = fields.Int(required=True)
    units = fields.Int(required=True)

    class Meta:
        strict = True

OrderState = {'delivered', 'onWay', 'cancelled', 'created'}

class OrderSchema(Schema):
    shop_id = fields.Int(required=True)
    products = fields.List(fields.Nested(OrderProductSchema), required=True)
    coordinates = fields.Nested(CoordinateSchema, required=True)
    payWithPoints = fields.Boolean(required=True)
    state = fields.Str(required=True, validate=lambda s: s in OrderState)
    user_id = fields.Int(required=True)

    @post_load
    def make_order_products(self, data, **kwargs):
        coordinates = data.pop('coordinates')
        products = data.pop('products')
        data['latitude'] = coordinates['latitude']
        data['longitude'] = coordinates['longitude']
        return data, products

    class Meta:
        strict = True

class StaticsDatetimeRangeSchema(Schema):
    year_from = fields.Int(required=True)
    month_from = fields.Int(required=True)
    year_to = fields.Int(required=True)
    month_to = fields.Int(required=True)

    class Meta:
        strict = True