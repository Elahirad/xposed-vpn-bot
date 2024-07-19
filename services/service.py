from models import Service, User, Server, Product
from typing import Optional
from services.hiddify import HiddifyInterface

def add_service(uuid: str, user_id: int, server_id:int, product_id:int) -> Service:
    user = User.get_or_none(User.id == user_id)
    product = Product.get_or_none(Product.id == product_id)
    server = Server.get_or_none(Server.id == server_id)
    service = Service.create(uuid=uuid, user=user, server=server, product=product)
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
        hid_service['raw_id'] = service.id
        services.append(hid_service)
    return services
        