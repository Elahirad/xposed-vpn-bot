from peewee import BigIntegerField, ForeignKeyField, CharField

from .base import BaseModel
from .server import Server


class Product(BaseModel):
    id = BigIntegerField(primary_key=True)

    name = CharField(unique=True)

    server = ForeignKeyField(Server, backref='products', on_delete='RESTRICT')

    days = BigIntegerField()

    gb_limit = BigIntegerField()

    price = BigIntegerField()

    class Meta:
        table_name = 'products'
