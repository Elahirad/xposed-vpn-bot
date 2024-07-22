from peewee import fn, JOIN

from models import Card, Receipt


def get_best_card() -> Card:
    approved_receipts = Receipt.select(Receipt.id, Receipt.approved, Receipt.card).where(
        Receipt.approved == True).alias('approved_receipts')

    query = (Card
             .select(Card)
             .join(approved_receipts, JOIN.LEFT_OUTER, on=(Card.id == approved_receipts.c.card_id))
             .group_by(Card)
             .order_by(fn.COUNT(approved_receipts.c.id).asc()))

    return list(query)[0]


def get_card(card_id: int) -> Card:
    query = Card.get(Card.id == card_id)
    return query


def get_cards() -> list[Card]:
    query = Card.select()
    return list(query)


def add_card(number: str):
    if Card.get_or_none(Card.number == number):
        Card.update({Card.is_active: True}).where(Card.number == number).execute()
        return Card.get_or_none(Card.number == number)
    return Card.create(number=number, is_active=True)


def disable_card(card_id: int):
    return Card.update({Card.is_active: False}).where(Card.id == card_id).execute()


def activate_card(card_id: int):
    return Card.update({Card.is_active: True}).where(Card.id == card_id).execute()
