from sqlalchemy import select

from database.connection import new_session
from database.models.user import UserRoleTable
from schemas.user import SUserRoleAdd, SUserRole

from fastapi.encoders import jsonable_encoder


class UserRoleRepository:
    @classmethod
    async def add_one(cls, data: UserRoleTable) -> int:
        async with new_session() as session:
            album_type_dict = data.model_dump()
            print(album_type_dict)
            album_type = UserRoleTable(**album_type_dict)
            session.add(album_type)
            await session.flush()
            await session.commit()
            return album_type.id

    @classmethod
    async def find_all(cls) -> list[SUserRole]:
        async with new_session() as session:
            query = select(UserRoleTable)
            result = await session.execute(query)
            album_type_models = result.scalars().all()
            album_type_shemas = [SUserRole.model_validate(jsonable_encoder(album_type_model)) for album_type_model in
                                 album_type_models]
            return album_type_shemas
