from peewee import BigIntegerField, CharField

from .base import BaseModel


class Server(BaseModel):
    id = BigIntegerField(primary_key=True)

    name = CharField(unique=True)

    url = CharField(unique=True)

    proxy_path = CharField()

    admin_uuid = CharField()

    class Meta:
        table_name = 'servers'
