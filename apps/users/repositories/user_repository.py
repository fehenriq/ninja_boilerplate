import uuid

from apps.users.models import Group, User


class UserRepository:
    @staticmethod
    def get_by_id(user_id: uuid.UUID) -> User | None:
        return User.objects.filter(pk=user_id).first()

    @staticmethod
    def get_by_email(email: str) -> User | None:
        return User.objects.filter(email=email).first()

    @staticmethod
    def update_or_create(pk: uuid.UUID, defaults: dict) -> tuple[User, bool]:
        return User.objects.update_or_create(id=pk, defaults=defaults)

    @staticmethod
    def set_groups(user: User, group_ids: list[uuid.UUID]):
        user.groups.set(Group.objects.filter(id__in=group_ids))

    @staticmethod
    def filter_by_groups(groups):
        return User.objects.filter(groups__in=groups).distinct()

    @staticmethod
    def all():
        return User.objects.all()
