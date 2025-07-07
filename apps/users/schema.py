import uuid

from ninja import Schema


class DepartmentSchema(Schema):
    id: uuid.UUID
    name: str
    company: str


class GroupSchema(Schema):
    id: uuid.UUID
    name: str


class UserSchema(Schema):
    id: uuid.UUID
    email: str
    name: str
    company: str
    department: DepartmentSchema
    theme: str
    color: str
    picture: str | None = None
    groups: list[GroupSchema] = []


class UserGroupSchema(Schema):
    id: uuid.UUID
    name: str
    email: str
    company: str
