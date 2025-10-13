from ninja import NinjaAPI, Redoc

from apps.users.api import user_router

api = NinjaAPI(
    csrf=False,
    title="API",
    version="1.0.0",
    description="This is a API to manage data",
)


api.add_router("/users", user_router, tags=["Users"])
