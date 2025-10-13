import uuid
from http import HTTPStatus

from apps.users.repositories.group_repository import GroupRepository
from apps.users.repositories.user_repository import UserRepository
from ninja.errors import HttpError

from apps.users.models import Group
from apps.users.schema import GroupSchema, UserGroupSchema
from utils.gimix_service import GIMIxService


class GroupService:
    def __init__(self):
        self.gimix_service = GIMIxService()
        self.repository = GroupRepository()

    def get_group_by_id(self, group_id: uuid.UUID) -> Group:
        return self.repository.get_by_id(group_id)

    def get_group_by_name(self, group_name: str) -> Group:
        return self.repository.get_by_name(group_name)

    def get_group(self, group_id: uuid.UUID) -> GroupSchema:
        if not (group := self.get_group_by_id(group_id)):
            raise HttpError(HTTPStatus.NOT_FOUND, "Grupo não encontrado")

        return group

    def sync_groups(self, token: str):
        groups = self.gimix_service.get_groups(token)
        for grp in groups.get("groups", []):
            self.repository.update_or_create(
                pk=uuid.UUID(grp["id"]),
                defaults={"name": grp["name"]},
            )

    def get_users_in_group(self, group_id: uuid.UUID) -> list[UserGroupSchema]:
        group = self.get_group(group_id)
        users = UserRepository.filter_by_groups([group])
        return [UserGroupSchema.from_orm(user) for user in users]

    def get_admin_users(self) -> list[UserGroupSchema]:
        group_names = ["Eng. Inovação", "Processos", "EngenhaDev", "SCI"]
        groups = self.repository.filter_by_names(group_names)
        users = UserRepository.filter_by_groups(groups)
        return [UserGroupSchema.from_orm(user) for user in users]
