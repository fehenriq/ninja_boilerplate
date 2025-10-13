import uuid

from ninja import Router
from ninja.errors import HttpError

from apps.users.schema import DepartmentSchema, GroupSchema, UserGroupSchema, UserSchema
from apps.users.services.department_service import DepartmentService
from apps.users.services.group_service import GroupService
from apps.users.services.user_service import UserService
from utils.jwt import JWTAuth, decode_jwt_token

user_router = Router(auth=JWTAuth())
group_router = Router(auth=JWTAuth())
department_router = Router(auth=JWTAuth())
user_service = UserService()
group_service = GroupService()
department_service = DepartmentService()


@user_router.post("/sync")
def sync_users(request):
    try:
        decode_jwt_token(request.headers.get("Authorization"))
        token = request.headers.get("Authorization").split(" ")[1]
        user_service.sync_users(token)
        return {"success": True, "message": "Usuários sincronizados com sucesso!"}
    except Exception as e:
        raise HttpError(500, f"Erro ao sincronizar usuários: {str(e)}") from e


@user_router.get("/{user_id}", response=UserSchema)
def retrieve_user(request, user_id: uuid.UUID):
    decode_jwt_token(request.headers.get("Authorization"))
    return user_service.get_user(user_id)


@group_router.post("/sync")
def sync_groups(request):
    try:
        decode_jwt_token(request.headers.get("Authorization"))
        token = request.headers.get("Authorization").split(" ")[1]
        group_service.sync_groups(token)
        return {"success": True, "message": "Grupos sincronizados com sucesso!"}
    except Exception as e:
        raise HttpError(500, f"Erro ao sincronizar grupos: {str(e)}") from e


@group_router.get("/{group_id}", response=GroupSchema)
def retrieve_group(request, group_id: uuid.UUID):
    decode_jwt_token(request.headers.get("Authorization"))
    return group_service.get_group(group_id)


@group_router.get("/{group_id}/users", response=list[UserGroupSchema], auth=None)
def retrieve_users_in_group(request, group_id: uuid.UUID):
    return group_service.get_users_in_group(group_id)


@group_router.get("/users/admins", response=list[UserGroupSchema], auth=None)
def retrieve_users_admins(request):
    return group_service.get_admin_users()


@department_router.get("", response=list[DepartmentSchema], auth=None)
def list_departments(request, company: str = None):
    return department_service.list_departments(company=company)


@department_router.post("/sync")
def sync_departments(request):
    try:
        decode_jwt_token(request.headers.get("Authorization"))
        token = request.headers.get("Authorization").split(" ")[1]
        department_service.sync_departments(token)
        return {"success": True, "message": "Departamentos sincronizados com sucesso!"}
    except Exception as e:
        raise HttpError(500, f"Erro ao sincronizar departamentos: {str(e)}") from e


@department_router.get("/{department_id}", response=DepartmentSchema)
def retrieve_department(request, department_id: uuid.UUID):
    decode_jwt_token(request.headers.get("Authorization"))
    return department_service.get_department(department_id)
