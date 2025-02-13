from typing import Optional

from models import Service, User, Server, Product
from services.hiddify import HiddifyInterface


def add_service(uuid: str, user_id: int, server_id: int, product_id: int, is_test_service: bool) -> Service:
    user = User.get_or_none(User.id == user_id)
    product = Product.get_or_none(Product.id == product_id)
    server = Server.get_or_none(Server.id == server_id)
    service = Service.create(uuid=uuid, user=user, server=server, product=product, is_test_service=is_test_service)
    return service


def get_service(service_id: int) -> Optional[Service]:
    return Service.get_or_none(Service.id == service_id)


def remove_service(service_id: int) -> None:
    Service.delete().where(Service.id == service_id).execute()


def get_user_services(user_id: int) -> list:
    user = User.get_or_none(User.id == user_id)
    query = Service.filter(Service.user == user)
    services_uuid = list(query)
    services = []
    for service in services_uuid:
        hiddify = HiddifyInterface(service.server.url,
                                   service.server.proxy_path,
                                   service.server.users_path,
                                   service.server.admin_uuid
                                   )
        hid_service = hiddify.get_service(service.uuid)
        if hid_service:
            hid_service['raw_id'] = service.id
            services.append(hid_service)
        else:
            Service.delete().where(Service.id == service.id).execute()
    return services


def is_test_service(uuid: str) -> bool:
    return Service.get_or_none(Service.uuid == uuid).is_test_service
