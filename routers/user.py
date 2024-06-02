from fastapi_users import fastapi_users, FastAPIUsers

from fastapi import FastAPI, Request, status, Depends, APIRouter, HTTPException

from auth.auth import auth_backend
from database.models import UserTable
from auth.manager import get_user_manager
from schemas.user import SUserRead, SUserCreate, SUserUpdate

from fastapi import APIRouter
from fastapi import Depends
from typing_extensions import Annotated

from repositories.user import UserRoleRepository, UserFollowRepository, UserProfileRepository
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


@router.post("/follow/{id}")
async def follow_user_by_id(id: int, user: UserTable = Depends(current_user)):
    if user.id == id:
        raise HTTPException(status_code=403, detail="Can't follow yourself")
    else:
        result = await UserFollowRepository.add_one(user_id=user.id, following_id=id)
        return result

@router.get("/profile/{id}")
async def get_user_profile(id: int, user: UserTable = Depends(current_user)):
    user_profile = await UserProfileRepository.find_by_id(id)
    return user_profile

@router.get("/followers/{id}")
async def get_user_followers(id: int, user: UserTable = Depends(current_user)):
    user_followers = await UserFollowRepository.find_all_followers(id)
    return user_followers


@router.get("/follows/{id}")
async def get_user_follows(id: int, user: UserTable = Depends(current_user)):
    user_followings = await UserFollowRepository.find_all_follows(id)
    return user_followings


@router.get("/role")
async def get_user_roles(user: UserTable = Depends(current_user)) -> list[SUserRole]:
    user_roles = await UserRoleRepository.find_all()
    return user_roles


@router.get("/role/{id}")
async def get_user_role_by_id(id: int, user: UserTable = Depends(current_user)) -> SUserRole:
    user_roles = await UserRoleRepository.find_by_id(id)
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
auth_router.include_router(fastapi_users.get_users_router(SUserRead, SUserUpdate))

router.include_router(auth_router)
router.include_router(auth_jwt_router)
