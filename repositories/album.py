from sqlalchemy import select

from database.connection import new_session
from database.models.album import AlbumTypeTable
from schemas.album import SAlbumTypeAdd, SAlbumType

from fastapi.encoders import jsonable_encoder


class AlbumTypeRepository:
    @classmethod
    async def add_one(cls, data: SAlbumTypeAdd) -> int:
        async with new_session() as session:
            album_type_dict = data.model_dump()
            print(album_type_dict)
            album_type = AlbumTypeTable(**album_type_dict)
            session.add(album_type)
            await session.flush()
            await session.commit()
            return album_type.id

    @classmethod
    async def find_all(cls) -> list[SAlbumType]:
        async with new_session() as session:
            query = select(AlbumTypeTable)
            result = await session.execute(query)
            album_type_models = result.scalars().all()
            album_type_shemas = [SAlbumType.model_validate(jsonable_encoder(album_type_model)) for album_type_model in
                                 album_type_models]
            return album_type_shemas
