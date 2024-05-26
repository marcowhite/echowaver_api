from sqlalchemy import select

from database.connection import new_session
from database.models.user import UserRoleTable
from database.models.user import UserFollowTable
from schemas.user import SUserRoleAdd, SUserRole

from fastapi.encoders import jsonable_encoder


class UserRoleRepository:
    @classmethod
    async def add_one(cls, data: SUserRoleAdd) -> int:
        async with new_session() as session:
            user_role_dict = data.model_dump()
            print(user_role_dict)
            user_role = UserRoleTable(**user_role_dict)
            session.add(user_role)
            await session.flush()
            await session.commit()
            return user_role.id

    @classmethod
    async def find_all(cls) -> list[SUserRole]:
        async with new_session() as session:
            query = select(UserRoleTable)
            result = await session.execute(query)
            user_role_models = result.scalars().all()
            user_role_shemas = [SUserRole.model_validate(jsonable_encoder(user_role_model)) for user_role_model in
                                user_role_models]
            return user_role_shemas

    @classmethod
    async def find_by_id(cls, id: int) -> SUserRole:
        async with new_session() as session:
            query = select(UserRoleTable).filter(UserRoleTable.id == id)
            result = await session.execute(query)
            user_role_model = result.scalars().first()
            user_role_schema = SUserRole.model_validate(jsonable_encoder(user_role_model))
            return user_role_schema


class UserFollowRepository:
    @classmethod
    async def add_one(cls, user_id: int, following_id: int):
        async with new_session() as session:
            user_follow = UserFollowTable(user_id=user_id, following_id=following_id)
            session.add(user_follow)
            await session.flush()
            await session.commit()
            return user_follow

    @classmethod
    async def find_all_follows(cls, user_id: int):
        async with new_session() as session:
            query = select(UserFollowTable).filter(UserFollowTable.user_id == user_id)
            result = await session.execute(query)
            user_follow_models = result.scalars().all()
            #user_role_schema = SUserRole.model_validate(jsonable_encoder(user_role_model))
            return user_follow_models

    @classmethod
    async def find_all_followers(cls, following_id: int):
        async with new_session() as session:
            query = select(UserFollowTable).filter(UserFollowTable.following_id == following_id)
            result = await session.execute(query)
            user_follow_models = result.scalars().all()
            #user_role_schema = SUserRole.model_validate(jsonable_encoder(user_role_model))
            return user_follow_models