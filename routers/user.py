from fastapi_users import fastapi_users, FastAPIUsers

from fastapi import FastAPI, Request, status, Depends, APIRouter, HTTPException

from auth.auth import auth_backend
from database.models import UserTable
from auth.manager import get_user_manager
from schemas.user import SUserRead, SUserCreate


from fastapi import APIRouter
from fastapi import Depends
from typing_extensions import Annotated

from repositories.user import UserRoleRepository
from schemas.user import SUserRoleAdd, SUserRole

router = APIRouter(
    prefix='/user',
    tags=['User']
)


fastapi_users = FastAPIUsers[UserTable, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()

@router.post("/role")
async def set_user_role(
        album_type: Annotated[SUserRoleAdd, Depends()],
        user: UserTable = Depends(current_user)
    ):
    if user.is_superuser:
        user_role_id = await UserRoleRepository.add_one(album_type)
        return {'response': True, 'user_role_id': user_role_id}
    else:
        raise HTTPException(status_code=403, detail="Unauthorized")

@router.get("/role")
async def get_user_roles() -> list[SUserRole]:
    user_roles = await UserRoleRepository.find_all()
    return user_roles

auth_jwt_router = APIRouter(
    prefix="/auth/jwt",
    tags=["User"],
)
auth_jwt_router.include_router(fastapi_users.get_auth_router(auth_backend))

auth_router = APIRouter(
    prefix="/auth",
    tags=["User"],
)

auth_router.include_router(fastapi_users.get_register_router(SUserRead, SUserCreate))

router.include_router(auth_router)
router.include_router(auth_jwt_router)