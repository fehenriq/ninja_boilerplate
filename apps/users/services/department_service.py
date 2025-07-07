import uuid
from http import HTTPStatus

from ninja.errors import HttpError

from apps.users.models import Department
from apps.users.schema import DepartmentSchema
from utils.gimix_service import GIMIxService


class DepartmentService:
    def __init__(self):
        self.gimix_service = GIMIxService()

    def get_department_by_id(self, department_id: uuid.UUID) -> Department:
        return Department.objects.filter(pk=department_id).first()

    def get_department(self, department_id: uuid.UUID) -> DepartmentSchema:
        if not (department := self.get_department_by_id(department_id)):
            raise HttpError(HTTPStatus.NOT_FOUND, "Departamento não encontrado")

        return department

    def sync_departments(self, token: str):
        departments = self.gimix_service.get_departments(token)

        for dept in departments.get("departments", []):
            Department.objects.update_or_create(
                id=uuid.UUID(dept["id"]),
                defaults={"name": dept["name"], "company": dept["company"]},
            )
