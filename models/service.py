from peewee import BigIntegerField, CharField, ForeignKeyField

from .base import BaseModel
from .user import User


class Service(BaseModel):
    id = BigIntegerField(primary_key=True)

    user = ForeignKeyField(User, backref='services', on_delete='RESTRICT')

    link = CharField(null=False)

    class Meta:
        table_name = 'services'
