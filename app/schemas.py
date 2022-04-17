from app.models import *
from app import marshmallow as ma


class BrandsResponseSchema(ma.Schema):
    class Meta:
        model = Brand

    id = ma.Integer()
    name = ma.String()


class UserResponseSchema(ma.Schema):
    class Meta:
        model = Customer

    id = ma.Integer()
    login = ma.String()
