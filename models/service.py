from peewee import BigIntegerField, CharField, ForeignKeyField

from .base import BaseModel
from .user import User
from .server import Server
from .product import Product


class Service(BaseModel):
    id = BigIntegerField(primary_key=True)

    user = ForeignKeyField(User, backref='services', on_delete='RESTRICT')

    uuid = CharField(default='')

    product = ForeignKeyField(Product, backref='services', on_delete='RESTRICT')

    server = ForeignKeyField(Server, backref='services', on_delete='RESTRICT')

    class Meta:
        table_name = 'services'
