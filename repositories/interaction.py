from sqlalchemy import select, delete, and_

from database.connection import new_session

from database.models.interactions import SongLikeTable, SongRepostTable
from database.models.interactions import AlbumLikeTable, AlbumRepostTable

from fastapi.encoders import jsonable_encoder


class LikeRepository:
    @classmethod
    async def like_song(cls, liker_id: int, liked_id: int):
        async with new_session() as session:
            print(liker_id, liked_id)
            song_like = SongLikeTable(liked_id=liked_id, liker_id=liker_id)
            session.add(song_like)
            await session.flush()
            await session.commit()
            return song_like

    @classmethod
    async def like_album(cls, liker_id: int, liked_id: int):
        async with new_session() as session:
            print(liker_id, liked_id)
            album_like = AlbumLikeTable(liked_id=liked_id, liker_id=liker_id)
            session.add(album_like)
            await session.flush()
            await session.commit()
            return album_like

    @classmethod
    async def unlike_song(cls, liker_id: int, liked_id: int):
        async with new_session() as session:
            await session.flush()
            query = delete(SongLikeTable).where(
                and_(
                SongLikeTable.liker_id == liker_id,
                SongLikeTable.liked_id == liked_id)
            )
            result = await session.execute(query)
            await session.flush()
            await session.commit()
            return result

    @classmethod
    async def unlike_album(cls, liker_id: int, liked_id: int):
        async with new_session() as session:
            await session.flush()
            query = delete(AlbumLikeTable).where(
                and_(
                AlbumLikeTable.liker_id == liker_id,
                AlbumLikeTable.liked_id == liked_id)
            )
            result = await session.execute(query)
            await session.flush()
            await session.commit()
            return result

    @classmethod
    async def get_song_likes_by_id(cls, id: int):
        async with new_session() as session:
            query = select(SongLikeTable).filter(SongLikeTable.liked_id == id)
            result = await session.execute(query)
            song_like_models = result.scalars().all()
            # album_type_schema = SAlbumType.model_validate(jsonable_encoder(album_type_model))
            return song_like_models

    @classmethod
    async def get_album_likes_by_id(cls, id: int):
        async with new_session() as session:
            query = select(AlbumLikeTable).filter(AlbumLikeTable.liked_id == id)
            result = await session.execute(query)
            album_like_models = result.scalars().all()
            # album_type_schema = SAlbumType.model_validate(jsonable_encoder(album_type_model))
            return album_like_models

    @classmethod
    async def get_user_likes(cls, id: int):
        async with new_session() as session:
            query = select(AlbumLikeTable).filter(AlbumLikeTable.liker_id == id)
            result = await session.execute(query)
            album_like_models = result.scalars().all()
            query = select(SongLikeTable).filter(SongLikeTable.liker_id == id)
            result = await session.execute(query)
            song_like_models = result.scalars().all()
            # album_type_schema = SAlbumType.model_validate(jsonable_encoder(album_type_model))
            return {'song_like': song_like_models, 'album_like': album_like_models}


class RepostRepository:
    @classmethod
    async def repost_song(cls, reposter_id: int, reposted_id: int):
        async with new_session() as session:
            print(reposter_id, reposted_id)
            song_repost = SongRepostTable(reposter_id=reposter_id, reposted_id=reposted_id)
            session.add(song_repost)
            await session.flush()
            await session.commit()
            return song_repost

    @classmethod
    async def repost_album(cls, reposter_id: int, reposted_id: int):
        async with new_session() as session:
            print(reposter_id, reposted_id)
            album_repost = AlbumRepostTable(reposter_id=reposter_id, reposted_id=reposted_id)
            session.add(album_repost)
            await session.flush()
            await session.commit()
            return album_repost

    @classmethod
    async def unrepost_song(cls, reposter_id: int, reposted_id: int):
        async with new_session() as session:
            await session.flush()
            query = delete(SongRepostTable).where(
                and_(
                SongRepostTable.reposter_id == reposter_id,
                SongRepostTable.reposted_id == reposted_id)
            )
            result = await session.execute(query)
            await session.flush()
            await session.commit()
            return result

    @classmethod
    async def unrepost_album(cls, reposter_id: int, reposted_id: int):
        async with new_session() as session:
            await session.flush()
            query = delete(AlbumLikeTable).where(
                and_(
                AlbumRepostTable.reposter_id == reposter_id,
                AlbumRepostTable.reposted_id == reposted_id)
            )
            result = await session.execute(query)
            await session.flush()
            await session.commit()
            return result
    @classmethod
    async def get_song_reposts_by_id(cls, id: int):
        async with new_session() as session:
            query = select(SongRepostTable).filter(SongRepostTable.reposted_id == id)
            result = await session.execute(query)
            song_repost_models = result.scalars().all()
            # album_type_schema = SAlbumType.model_validate(jsonable_encoder(album_type_model))
            return song_repost_models

    @classmethod
    async def get_album_reposts_by_id(cls, id: int):
        async with new_session() as session:
            query = select(AlbumRepostTable).filter(AlbumRepostTable.reposted_id == id)
            result = await session.execute(query)
            album_repost_models = result.scalars().all()
            # album_type_schema = SAlbumType.model_validate(jsonable_encoder(album_type_model))
            return album_repost_models

    @classmethod
    async def get_user_reposts(cls, id: int):
        async with new_session() as session:
            query = select(AlbumRepostTable).filter(AlbumRepostTable.reposter_id == id)
            result = await session.execute(query)
            album_repost_models = result.scalars().all()
            query = select(SongRepostTable).filter(SongRepostTable.reposter_id == id)
            result = await session.execute(query)
            song_repost_models = result.scalars().all()
            # album_type_schema = SAlbumType.model_validate(jsonable_encoder(album_type_model))
            return {'song_repost': album_repost_models, 'album_repost': song_repost_models}
