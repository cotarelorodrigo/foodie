from marshmallow import Schema, fields


class UserSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    signup_date = fields.DateTime(required=True)
    firebase_uid = fields.Str(required=True)
    picture = fields.Str(required=False)

    class Meta:
        strict = True
        fields = ('fullName', 'email', 'password', 'signUpDate', 'firebaseUid', 'picture')


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

class ItemSchema(Schema):
    id = fields.Int(required=True)
    units = fields.Int(required=True)

    class Meta:
        strict = True

class CoordinateSchema(Schema):
    latitude = fields.Float(required=True)
    longitude = fields.Float(required=True)

    class Meta:
        strict = True

class OrderSchema(Schema):
    shopId = fields.Int(required=True)
    items = fields.List(fields.Nested(ItemSchema), required=True)
    coordinates = fields.Nested(CoordinateSchema, required=True)
    payWithPoints = fields.Boolean(required=True)

    class Meta:
        strict = True