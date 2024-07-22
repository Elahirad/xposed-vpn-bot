from peewee import BigIntegerField, CharField, BooleanField

from .base import BaseModel


class Card(BaseModel):
    id = BigIntegerField(primary_key=True)

    number = CharField()

    is_active = BooleanField()

    class Meta:
        table_name = 'cards'
