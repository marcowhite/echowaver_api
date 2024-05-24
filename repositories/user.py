from sqlalchemy import select

from database.connection import new_session
from database.models.user import UserRoleTable
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
