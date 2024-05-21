from sqlalchemy import select

from database.connection import new_session
from database.models.song import TagsTable
from schemas.song import SSongTagsAdd, SSongsTags

from fastapi.encoders import jsonable_encoder


class SongTagRepository:
    @classmethod
    async def add_one(cls, data: SSongTagsAdd) -> int:
        async with new_session() as session:
            song_tag_dict = data.model_dump()
            print(song_tag_dict)
            song_tag = TagsTable(**song_tag_dict)
            session.add(song_tag)
            await session.flush()
            await session.commit()
            return song_tag.id

    @classmethod
    async def find_all(cls) -> list[SSongsTags]:
        async with new_session() as session:
            query = select(TagsTable)
            result = await session.execute(query)
            song_tag_models = result.scalars().all()
            song_tag_shemas = [SSongsTags.model_validate(jsonable_encoder(song_tag_model)) for song_tag_model in
                                 song_tag_models]
            return song_tag_shemas
