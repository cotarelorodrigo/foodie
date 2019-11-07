from marshmallow import Schema, fields


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


class ShopSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    address = fields.Str(required=True)
    description = fields.Str(required=True)
    photoUrl = fields.Str(required=True)
    rating = fields.Int(required=True)
    #To do: Falta meter el campo menu, que seria?


    class Meta:
        strict = True
        fields = ('id', 'name', 'address', 'description', 'photoUrl', 'rating')

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

class CoordinateSchema(Schema):
    latitude = fields.Float(required=True)
    longitude = fields.Float(required=True)

    class Meta:
        strict = True

class OrderSchema(Schema):
    shop_id = fields.Int(required=True)
    products = fields.List(fields.Nested(OrderProductSchema), required=True)
    coordinates = fields.Nested(CoordinateSchema, required=True)
    payWithPoints = fields.Boolean(required=True)

    class Meta:
        strict = True