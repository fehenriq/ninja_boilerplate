import uuid
from http import HTTPStatus

from apps.users.repositories.user_repository import UserRepository
from ninja.errors import HttpError

from apps.users.models import User
from apps.users.schema import UserSchema
from apps.users.services.department_service import DepartmentService
from apps.users.services.group_service import GroupService
from utils.gimix_service import GIMIxService


class UserService:
    def __init__(self):
        self.gimix_service = GIMIxService()
        self.department_service = DepartmentService()
        self.group_service = GroupService()
        self.repository = UserRepository()

    def get_user_by_id(self, user_id: uuid.UUID) -> User:
        return self.repository.get_by_id(user_id)

    def get_user_by_email(self, email: str) -> User:
        return self.repository.get_by_email(email)

    def get_user(self, user_id: uuid.UUID) -> UserSchema:
        if not (user := self.get_user_by_id(user_id)):
            raise HttpError(HTTPStatus.NOT_FOUND, "Usuário não encontrado")

        return user

    def sync_users(self, token: str):
        users = self.gimix_service.get_users(token)
        for usr in users.get("users", []):
            department_data = usr["department"]
            department = self.department_service.get_department(department_data["id"])
            user, _ = self.repository.update_or_create(
                pk=uuid.UUID(usr["id"]),
                defaults={
                    "email": usr["email"],
                    "name": usr["name"],
                    "company": usr["company"],
                    "department": department,
                    "theme": usr["theme"],
                    "color": usr["color"],
                    "picture": usr["picture"],
                },
            )
            groups_list = [group["id"] for group in usr["groups"]]
            self.repository.set_groups(user, groups_list)
