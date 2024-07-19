from typing import Optional

from models import Product, Server


def get_products() -> Optional[list[Product]]:
    query = Product.select()
    return list(query)


def find_product(name: str) -> Optional[Product]:
    query = Product.get(Product.name == name)
    return query


def add_product(name: str, server_name: str, days: int, gb_limit: int, price: int) -> Product:
    server = Server.get_or_none(Server.name == server_name)
    product = Product.create(name=name, server=server, days=days, gb_limit=gb_limit, price=price)
    return product


def delete_product(product_id: int) -> None:
    Product.delete().where(Product.id == product_id).execute()


def update_product_name(product_id: int, name: str) -> None:
    Product.update({Product.name: name}).where(Product.id == product_id).execute()


def update_product_server(product_id: int, server_name: str) -> None:
    server = Server.get_or_none(Server.name == server_name)
    Product.update({Product.server: server}).where(Product.id == product_id).execute()


def update_product_days(product_id: int, days: int) -> None:
    Product.update({Product.days: days}).where(Product.id == product_id).execute()


def update_product_gb_limit(product_id: int, gb_limit: int) -> None:
    Product.update({Product.gb_limit: gb_limit}).where(Product.id == product_id).execute()


def update_product_price(product_id: int, price: int) -> None:
    Product.update({Product.price: price}).where(Product.id == product_id).execute()
