from uuid import UUID

from ninja import Schema


class BaseSchema(Schema):
    id: UUID
    created_at: str
    updated_at: str
    deleted_at: str | None


class ErrorSchema(Schema):
    detail: str
