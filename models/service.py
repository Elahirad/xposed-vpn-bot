import datetime

from peewee import BigIntegerField, CharField, ForeignKeyField, DateTimeField, BooleanField

from .base import BaseModel
from .product import Product
from .server import Server
from .user import User


class Service(BaseModel):
    id = BigIntegerField(primary_key=True)

    user = ForeignKeyField(User, backref='services', on_delete='RESTRICT')

    uuid = CharField(default='')

    product = ForeignKeyField(Product, backref='services', on_delete='RESTRICT', null=True)

    server = ForeignKeyField(Server, backref='services', on_delete='RESTRICT')

    created_at = DateTimeField(default=datetime.datetime.now())

    is_test_service = BooleanField(default=False)

    class Meta:
        table_name = 'services'
