from sqlalchemy import select, delete

from database.connection import new_session
from database.models.song import SongTagTable, SongListenTable
from schemas.song import SSongTagAdd, SSongTag, SSongListenAdd, SSongListen

from database.models.song import SongTable
from schemas.song import SSongAdd, SSong

from fastapi.encoders import jsonable_encoder


class SongRepository:
    @classmethod
    async def add_one(cls, data: SSongAdd, audio_file: str, cover_file: str, user_id: int) -> int:
        async with new_session() as session:
            song_dict = data.model_dump()
            song_dict.update(audio_file=audio_file)
            song_dict.update(cover_file=cover_file)
            song_dict.update(user_id=user_id)
            print(song_dict)
            song = SongTable(**song_dict)
            session.add(song)
            await session.flush()
            await session.commit()
            return song.id

    @classmethod
    async def delete_by_id(cls, id: int):
        async with new_session() as session:
            await session.flush()
            query = delete(SongTable).filter(SongTable.id == id)
            result = await session.execute(query)
            await session.flush()
            await session.commit()
            return result

    @classmethod
    async def update_by_id(cls, id: int, data: SSongAdd) -> SSong:
        async with new_session() as session:
            async with session.begin():
                query = select(SongTable).filter(SongTable.id == id).with_for_update()
                result = await session.execute(query)
                song = result.scalar_one_or_none()

                song_dict = data.model_dump()
                for key, value in song_dict.items():
                    setattr(song, key, value)

                await session.commit()
                return song
    @classmethod
    async def find_all(cls) -> list[SSong]:
        async with new_session() as session:
            query = select(SongTable)
            result = await session.execute(query)
            song_models = result.scalars().all()
            song_shemas = [SSong.model_validate(jsonable_encoder(song_model)) for song_model in
                           song_models]
            return song_shemas

    @classmethod
    async def find_by_id(cls, id: int) -> SSong:
        async with new_session() as session:
            query = select(SongTable).filter(SongTable.id == id)
            result = await session.execute(query)
            song_model = result.scalars().first()
            song_shemas = SSong.model_validate(jsonable_encoder(song_model))
            return song_shemas

    @classmethod
    async def find_all_by_user_id(cls, user_id: int) -> list[SSong]:
        async with new_session() as session:
            query = select(SongTable).filter(SongTable.user_id == user_id)
            result = await session.execute(query)
            song_models = result.scalars().all()
            song_shemas = [SSong.model_validate(jsonable_encoder(song_model)) for song_model in
                           song_models]
            return song_shemas


class SongTagRepository:
    @classmethod
    async def add_one(cls, data: SSongTagAdd) -> int:
        async with new_session() as session:
            song_tag_dict = data.model_dump()
            print(song_tag_dict)
            song_tag = SongTagTable(**song_tag_dict)
            session.add(song_tag)
            await session.flush()
            await session.commit()
            return song_tag.id

    @classmethod
    async def find_by_song_id(cls, song_id: int) -> list[SSongTag]:
        async with new_session() as session:
            query = select(SongTagTable).filter(SongTagTable.song_id == song_id)
            result = await session.execute(query)
            song_tag_models = result.scalars().all()
            song_tag_shemas = [SSongTag.model_validate(jsonable_encoder(song_tag_model)) for song_tag_model in
                               song_tag_models]
            return song_tag_shemas


class SongListenRepository:
    @classmethod
    async def add_one(cls, data: SSongListenAdd, user_id: int) -> int:
        async with new_session() as session:
            song_listen_dict = data.model_dump()
            song_listen_dict.update(user_id=user_id)
            print(song_listen_dict)
            song_listen = SongListenTable(**song_listen_dict)
            session.add(song_listen)
            await session.flush()
            await session.commit()
            return song_listen.id

    @classmethod
    async def find_by_song_id(cls, song_id: int) -> list[SSongListen]:
        async with new_session() as session:
            query = select(SongListenTable).filter(SongListenTable.song_id == song_id)
            result = await session.execute(query)
            song_listen_models = result.scalars().all()
            song_listen_shemas = [SSongListen.model_validate(jsonable_encoder(song_listen_model)) for song_listen_model in
                               song_listen_models]
            return song_listen_shemas
