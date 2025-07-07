import uuid
from http import HTTPStatus

from ninja.errors import HttpError

from apps.users.models import Group, User
from apps.users.schema import GroupSchema, UserGroupSchema
from utils.gimix_service import GIMIxService


class GroupService:
    def __init__(self):
        self.gimix_service = GIMIxService()

    def get_group_by_id(self, group_id: uuid.UUID) -> Group:
        return Group.objects.filter(pk=group_id).first()

    def get_group_by_name(self, group_name: str) -> Group:
        return Group.objects.filter(name=group_name).first()

    def get_group(self, group_id: uuid.UUID) -> GroupSchema:
        if not (group := self.get_group_by_id(group_id)):
            raise HttpError(HTTPStatus.NOT_FOUND, "Grupo não encontrado")

        return group

    def sync_groups(self, token: str):
        groups = self.gimix_service.get_groups(token)

        for grp in groups.get("groups", []):
            Group.objects.update_or_create(
                id=uuid.UUID(grp["id"]),
                defaults={"name": grp["name"]},
            )

    def get_users_in_group(self, group_id: uuid.UUID) -> list[UserGroupSchema]:
        group = self.get_group(group_id)

        users = User.objects.filter(groups=group)
        return [UserGroupSchema.from_orm(user) for user in users]
