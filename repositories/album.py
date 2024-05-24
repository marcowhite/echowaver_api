from sqlalchemy import select

from database.connection import new_session

from database.models.album import AlbumTypeTable
from schemas.album import SAlbumTypeAdd, SAlbumType

from database.models.album import AlbumTable
from schemas.album import SAlbumAdd, SAlbum

from fastapi.encoders import jsonable_encoder

class AlbumRepository:
    @classmethod
    async def add_one(cls, data: SAlbumAdd, user_id: int) -> int:
        async with new_session() as session:
            album_dict = data.model_dump()
            album_dict.update(user_id=user_id)
            print(album_dict)
            album = AlbumTable(**album_dict)
            session.add(album)
            await session.flush()
            await session.commit()
            return album.id

    @classmethod
    async def find_all(cls) -> list[SAlbum]:
        async with new_session() as session:
            query = select(AlbumTable)
            result = await session.execute(query)
            album_models = result.scalars().all()
            album_shemas = [SAlbum.model_validate(jsonable_encoder(album_model)) for album_model in
                                 album_models]
            return album_shemas

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
