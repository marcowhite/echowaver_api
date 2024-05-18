from sqlalchemy import select

from database.connection import new_session, SongTable
from schemas import SSongAdd, SSong
from fastapi.encoders import jsonable_encoder

class SongRepository:
    @classmethod
    async def add_one(cls, data: SSongAdd) -> int:
        async with new_session() as session:
            song_dict = data.model_dump()
            print(song_dict)
            song = SongTable(**song_dict)
            session.add(song)
            await session.flush()
            await session.commit()
            return song.id

    @classmethod
    async def find_all(cls) -> list[SSong]:
        async with new_session() as session:
            query = select(SongTable)
            result = await session.execute(query)
            song_models = result.scalars().all()
            song_schemas = [SSong.model_validate(jsonable_encoder(song_model)) for song_model in song_models]
            return song_schemas
