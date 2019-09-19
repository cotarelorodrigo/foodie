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