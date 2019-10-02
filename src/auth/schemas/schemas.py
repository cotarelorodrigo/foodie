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