from typing import Optional

from models import Server


def get_servers() -> Optional[list[Server]]:
    query = Server.select()
    return list(query)


def add_server(name: str, url: str, proxy_path: str, users_path: str, admin_uuid: str) -> Server:
    print("HEre")
    server = Server.create(name=name, url=url, proxy_path=proxy_path, users_path=users_path, admin_uuid=admin_uuid)
    return server


def delete_server(server_id: int) -> None:
    Server.delete().where(Server.id == server_id).execute()


def update_server_name(server_id: int, server_name: str) -> None:
    Server.update({Server.name: server_name}).where(Server.id == server_id).execute()


def update_server_url(server_id: int, url: str) -> None:
    Server.update({Server.url: url}).where(Server.id == server_id).execute()


def update_server_proxy_path(server_id: int, proxy_path: str) -> None:
    Server.update({Server.proxy_path: proxy_path}).where(Server.id == server_id).execute()


def update_server_admin_uuid(server_id: int, admin_uuid: str) -> None:
    Server.update({Server.admin_uuid: admin_uuid}).where(Server.id == server_id).execute()
