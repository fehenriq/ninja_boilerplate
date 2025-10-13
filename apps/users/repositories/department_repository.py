import uuid

from apps.users.models import Department


class DepartmentRepository:
    @staticmethod
    def get_by_id(department_id: uuid.UUID) -> Department | None:
        return Department.objects.filter(pk=department_id).first()

    @staticmethod
    def update_or_create(pk: uuid.UUID, defaults: dict) -> tuple[Department, bool]:
        return Department.objects.update_or_create(id=pk, defaults=defaults)

    @staticmethod
    def all(company: str | None = None):
        qs = Department.objects.all()
        if company:
            qs = qs.filter(company=company)
        return qs
