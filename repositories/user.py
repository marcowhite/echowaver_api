from sqlalchemy import select, delete, and_
from sqlalchemy.orm import joinedload

from database.connection import new_session
from database.models.user import UserRoleTable, UserTable
from database.models.user import UserFollowTable
from schemas.user import SUserRoleAdd, SUserRole, SUserProfile

from fastapi.encoders import jsonable_encoder

class UserProfileRepository:
    @classmethod
    async def find_by_id(cls, id: int) -> SUserProfile:
        async with new_session() as session:
            query = select(UserTable).filter(UserTable.id == id)
            result = await session.execute(query)
            user_profile_model = result.scalars().first()
            user_profile_schema = SUserProfile.model_validate(jsonable_encoder(user_profile_model))
            return user_profile_schema


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
    async def delete_by_id(cls, user_id: int, following_id: int):
        async with new_session() as session:
            await session.flush()
            query = delete(UserFollowTable).where(
                and_(
                    UserFollowTable.user_id == user_id,
                    UserFollowTable.following_id == following_id)
            )
            result = await session.execute(query)
            await session.flush()
            await session.commit()
            return result

    @classmethod
    async def find_all_follows(cls, user_id: int) -> list[SUserProfile]:
        async with new_session() as session:
            query = (
                select(UserFollowTable)
                .filter(UserFollowTable.user_id == user_id)
                .options(joinedload(UserFollowTable.following_user))
            )
            result = await session.execute(query)
            user_follow_models = result.scalars().all()

            # Получаем все профили пользователей, на которых подписан user_id
            user_models = [follow.following_user for follow in user_follow_models]

            # Преобразуем их в схему SUserProfile
            user_schemas = [SUserProfile.model_validate(jsonable_encoder(user)) for user in user_models]
            return user_schemas

    @classmethod
    async def find_all_followers(cls, following_id: int) -> list[SUserProfile]:
        async with new_session() as session:
            query = (
                select(UserFollowTable)
                .filter(UserFollowTable.following_id == following_id)
                .options(joinedload(UserFollowTable.user))
            )
            result = await session.execute(query)
            user_follow_models = result.scalars().all()

            # Получаем все профили пользователей, которые подписаны на following_id
            user_models = [follow.user for follow in user_follow_models]

            # Преобразуем их в схему SUserProfile
            user_schemas = [SUserProfile.model_validate(jsonable_encoder(user)) for user in user_models]
            return user_schemas