from marshmallow import Schema, fields


class UserSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Str(required=True)
    password = fields.Email(required=True)

    class Meta:
        strict = True
        fields = ('name', 'email')