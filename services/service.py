from models import Service, User


def add_service(uuid: str, user_id: int) -> Service:
    user = User.get_or_none(User.id == user_id)
    service = Service.create(uuid=uuid, user=user)
    return service
