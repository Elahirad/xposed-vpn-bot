from peewee import BigIntegerField, CharField, ForeignKeyField, BooleanField

from .base import BaseModel
from .user import User


class Receipt(BaseModel):
    id = BigIntegerField(primary_key=True)

    user = ForeignKeyField(User, backref='receipts')

    amount = BigIntegerField()

    receipt_photo = CharField()

    approved = BooleanField(default=False)

    rejected = BooleanField(default=False)

    class Meta:
        table_name = 'receipts'
