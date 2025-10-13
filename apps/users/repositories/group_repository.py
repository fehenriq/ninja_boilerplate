import uuid

from apps.users.models import Group


class GroupRepository:
    @staticmethod
    def get_by_id(group_id: uuid.UUID) -> Group | None:
        return Group.objects.filter(pk=group_id).first()

    @staticmethod
    def get_by_name(group_name: str) -> Group | None:
        return Group.objects.filter(name=group_name).first()

    @staticmethod
    def update_or_create(pk: uuid.UUID, defaults: dict) -> tuple[Group, bool]:
        return Group.objects.update_or_create(id=pk, defaults=defaults)

    @staticmethod
    def filter_by_names(names: list[str]):
        return Group.objects.filter(name__in=names)

    @staticmethod
    def all():
        return Group.objects.all()
