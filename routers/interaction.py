from fastapi import APIRouter, HTTPException
from fastapi import Depends
from typing_extensions import Annotated

from database.models import UserTable
from repositories.album import AlbumRepository
from repositories.interaction import LikeRepository, RepostRepository
from repositories.song import SongRepository
from routers.user import fastapi_users

router = APIRouter(
    prefix='',
    tags=['Interactions']
)

current_user = fastapi_users.current_user()


@router.post("/song/like/{id}")
async def like_song(liked_id: int, user: UserTable = Depends(current_user)):
    song = await SongRepository.find_by_id(liked_id)
    if song.is_public or song.user_id == user.id:
        song_like = await LikeRepository.like_song(liked_id=liked_id, liker_id=user.id)
        return song_like
    else:
        raise HTTPException(status_code=403, detail="You are not authorized to like this song")


@router.delete("/song/like/{id}")
async def unlike_song(liked_id: int, user: UserTable = Depends(current_user)):
    song_like = await LikeRepository.unlike_song(liked_id=liked_id, liker_id=user.id)
    return song_like


@router.post("/album/like/{id}")
async def like_album(liked_id: int, user: UserTable = Depends(current_user)):
    album = await AlbumRepository.find_by_id(liked_id)
    if album.is_public or album.user_id == user.id:
        album_like = await LikeRepository.like_album(liked_id=liked_id, liker_id=user.id)
        return album_like
    else:
        raise HTTPException(status_code=403, detail="You are not authorized to like this album")


@router.delete("/album/like/{id}")
async def unlike_album(liked_id: int, user: UserTable = Depends(current_user)):
    album_like = await LikeRepository.unlike_album(liked_id=liked_id, liker_id=user.id)
    return album_like
@router.get("/song/likes/{id}")
async def get_song_likes_by_id(id: int, user: UserTable = Depends(current_user)):
    song_likes = await LikeRepository.get_song_likes_by_id(id)
    return song_likes


@router.post("/song/repost/{id}")
async def repost_song(reposted_id: int, user: UserTable = Depends(current_user)):
    song = await SongRepository.find_by_id(reposted_id)
    if song.is_public or song.user_id == user.id:
        song_repost = await RepostRepository.repost_song(reposter_id=user.id, reposted_id=reposted_id)
        return song_repost
    else:
        raise HTTPException(status_code=403, detail="You are not authorized to repost this song")

@router.post("/album/repost/{id}")
async def repost_album(reposted_id: int, user: UserTable = Depends(current_user)):
    album = await AlbumRepository.find_by_id(reposted_id)
    if album.is_public or album.user_id == user.id:
        album_repost = await RepostRepository.repost_album(reposter_id=user.id, reposted_id=reposted_id)
        return album_repost
    else:
        raise HTTPException(status_code=403, detail="You are not authorized to repost this album")


@router.delete("/song/repost/{id}")
async def unrepost_song(reposted_id: int, user: UserTable = Depends(current_user)):
    song_repost = await RepostRepository.unrepost_song(reposter_id=user.id, reposted_id=reposted_id)
    return song_repost


@router.delete("/album/repost/{id}")
async def unrepost_album(reposted_id: int, user: UserTable = Depends(current_user)):
    album_repost = await RepostRepository.unrepost_album(reposter_id=user.id, reposted_id=reposted_id)
    return album_repost

@router.get("/song/reposts/{id}")
async def get_song_reposts_by_id(id: int, user: UserTable = Depends(current_user)):
    song_reposts = await RepostRepository.get_song_reposts_by_id(id)
    return song_reposts


@router.get("/album/reposts/{id}")
async def get_album_reposts_by_id(id: int, user: UserTable = Depends(current_user)):
    album_reposts = await RepostRepository.get_album_reposts_by_id(id)
    return album_reposts


@router.get("/user/reposts/{id}")
async def get_user_reposts(id: int, user: UserTable = Depends(current_user)):
    user_reposts = await RepostRepository.get_user_reposts(id=id)
    return user_reposts


@router.get("/user/likes/{id}")
async def get_user_likes(id: int, user: UserTable = Depends(current_user)):
    user_likes = await LikeRepository.get_user_likes(id=id)
    return user_likes
