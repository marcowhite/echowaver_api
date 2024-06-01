from sqlalchemy import select, delete

from database.connection import new_session

from database.models.album import AlbumTypeTable
from schemas.album import SAlbumTypeAdd, SAlbumType

from database.models.album import AlbumTable
from schemas.album import SAlbumAdd, SAlbum

from fastapi.encoders import jsonable_encoder


class AlbumRepository:
    @classmethod
    async def add_one(cls, data: SAlbumAdd,cover_file: str, user_id: int) -> int:
        async with new_session() as session:
            album_dict = data.model_dump()
            album_dict.update(user_id=user_id)
            album_dict.update(cover_file=cover_file)
            print(album_dict)
            album = AlbumTable(**album_dict)
            session.add(album)
            await session.flush()
            await session.commit()
            return album.id

    @classmethod
    async def delete_by_id(cls, id: int):
        async with new_session() as session:
            await session.flush()
            query = delete(AlbumTable).filter(AlbumTable.id == id)
            result = await session.execute(query)
            await session.flush()
            await session.commit()
            return result

    @classmethod
    async def find_all(cls) -> list[SAlbum]:
        async with new_session() as session:
            query = select(AlbumTable)
            result = await session.execute(query)
            album_models = result.scalars().all()
            album_shemas = [SAlbum.model_validate(jsonable_encoder(album_model)) for album_model in
                            album_models]
            return album_shemas

    @classmethod
    async def find_all_by_user_id(cls, user_id: int) -> list[SAlbum]:
        async with new_session() as session:
            query = select(AlbumTable).filter(AlbumTable.user_id == user_id)
            result = await session.execute(query)
            album_models = result.scalars().all()
            album_shemas = [SAlbum.model_validate(jsonable_encoder(album_model)) for album_model in
                            album_models]
            return album_shemas

    @classmethod
    async def find_by_id(cls, id: int) -> SAlbum:
        async with new_session() as session:
            query = select(AlbumTable).filter(AlbumTable.id == id)
            result = await session.execute(query)
            album_model = result.scalars().first()
            album_schema = SAlbum.model_validate(jsonable_encoder(album_model))
            return album_schema

    @classmethod
    async def update_by_id(cls, id: int, data: SAlbumAdd) -> SAlbum:
        async with new_session() as session:
            async with session.begin():
                query = select(AlbumTable).filter(AlbumTable.id == id).with_for_update()
                result = await session.execute(query)
                album = result.scalar_one_or_none()

                album_dict = data.model_dump()
                for key, value in album_dict.items():
                    setattr(album, key, value)

                await session.commit()
                return album


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

    @classmethod
    async def find_by_id(cls, id: int) -> SAlbumType:
        async with new_session() as session:
            query = select(AlbumTypeTable).filter(AlbumTypeTable.id == id)
            result = await session.execute(query)
            album_type_model = result.scalars().first()
            album_type_schema = SAlbumType.model_validate(jsonable_encoder(album_type_model))
            return album_type_schema
