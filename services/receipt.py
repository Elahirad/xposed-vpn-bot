from models import Receipt


def get_unresolved_receipts() -> list[Receipt]:
    query = Receipt.filter(Receipt.approved == False, Receipt.rejected == False)
    return list(query)


def get_receipt_by_id(receipt_id: int) -> Receipt:
    query = Receipt.get_or_none(Receipt.id == receipt_id)
    return query
