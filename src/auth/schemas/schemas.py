from marshmallow import Schema, fields, post_load, post_dump
import re


class UserSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    phone_number = fields.Int(required=True)
    #role = fields.String(required=True)
    password = fields.Str(required=False)
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
    reviews = fields.Float(required=False)
    rating = fields.Float(required=False)


    class Meta:
        strict = True

class CoordinateSchema(Schema):
    latitude = fields.Float(required=True)
    longitude = fields.Float(required=True)

    class Meta:
        strict = True

class ProductSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    price = fields.Int(required=True)

class ShopSchema(Schema):
    name = fields.Str(required=True)
    address = fields.Str(required=True)
    description = fields.Str(required=False)
    coordinates = fields.Nested(CoordinateSchema, required=True)
    photoUrl = fields.Str(required=True)
    rating = fields.Int(required=True)
    menu = fields.List(fields.Nested(ProductSchema), required=False)

    @post_load
    def make_order_products(self, data, **kwargs):
        coordinates = data.pop('coordinates')
        data['latitude'] = coordinates['latitude']
        data['longitude'] = coordinates['longitude']
        try:
            products = data.pop('menu')
        except:
            products = []
        return data, products

    class Meta:
        strict = True

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)

    class Meta:
        strict = True

class LoginSchemaToken(Schema):
    firebase_uid = fields.Str(required=True)

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

OrderOfferState = {'offered', 'accepted', 'rejected', 'cancelled'}

class OrderOfferSchema(Schema):
    order_id = fields.Int(required=True)
    delivery_id = fields.Int(required=True)
    delivery_price = fields.Float(required=True)
    delivery_pay = fields.Float(required=True)

    class Meta:
        strict = True

OrderState = {'delivered','pickedUp','onWay', 'cancelled', 'created'}

class FavourOfferSchema(Schema):
    order_id = fields.Int(required=True)
    user_id = fields.Int(required=True)
    points = fields.Int(required=True)


class OrderSchema(Schema):
    shop_id = fields.Int(required=True)
    products = fields.List(fields.Nested(OrderProductSchema), required=True)
    coordinates = fields.Nested(CoordinateSchema, required=True)
    payWithPoints = fields.Boolean(required=True)
    favourPoints = fields.Int(required=False)
    price = fields.Field(required=True)
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

def is_valid_card_number(sequence):
    """Returns `True' if the sequence is a valid credit card number.

    A valid credit card number
    - must contain exactly 16 digits,
    - must start with a 4, 5 or 6 
    - must only consist of digits (0-9) or hyphens '-',
    - may have digits in groups of 4, separated by one hyphen "-". 
    - must NOT use any other separator like ' ' , '_',
    - must NOT have 4 or more consecutive repeated digits.
    """
    PATTERN='^([456][0-9]{3})-?([0-9]{4})-?([0-9]{4})-?([0-9]{4})$'

    match = re.match(PATTERN,sequence)

    if match == None:
        return False

    # for group in match.groups():
        if group[0] * 4 == group:
            return False
    return True

class CreditCardSchema(Schema):

    number = fields.Str(required=True, validate=lambda s: is_valid_card_number(s))
    security_code = fields.Int(required=True)

    class Meta:
        strict = True