from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi import Depends
from typing_extensions import Annotated

from database.models import UserTable
from repositories.song import SongTagRepository, SongRepository
from routers.file import upload_audio, upload_image
from routers.user import fastapi_users
from schemas.song import SSongTagAdd, SSongTag, SSong, SSongAdd

router = APIRouter(
    prefix='/song',
    tags=['Songs']
)

current_user = fastapi_users.current_user()


@router.post("")
async def add_song(
        song: Annotated[SSongAdd, Depends()],
        audio_file: UploadFile = File(...),
        image_file: UploadFile = File(...),
        user: UserTable = Depends(current_user)
):
    try:
        audio_responce = await upload_audio(audio_file)
        image_responce = await upload_image(image_file)
    except Exception as e:
        raise e

    song_id = await SongRepository.add_one(song, user_id=user.id, audio_file=audio_responce['message'],
                                           cover_file=image_responce['message'])

    return {'response': True, 'song_id': song_id}


@router.get("/{id}")
async def get_song_by_id(
        id: int,
        user: UserTable = Depends(current_user)
) -> SSong:
    song = await SongRepository.find_by_id(id)

    if song.is_public:
        return song
    else:
        if user.id == song.user_id:
            return song
        else:
            return []


@router.delete("/{id}")
async def delete_song_by_id(
        id: int,
        user: UserTable = Depends(current_user)
):
    song = await get_song_by_id(id, user)
    if song.user_id == user.id:
        result = await SongRepository.delete_by_id(id)
        return {"responce": True}
    else:
        return {"responce": False}


@router.get("/user/{user_id}")
async def get_songs_by_user_id(
        user_id: int,
        user: UserTable = Depends(current_user)
) -> list[SSong]:
    songs = await SongRepository.find_all_by_user_id(user_id)
    if user.id != user_id:
        songs = list(filter(lambda x: x.is_public == True, songs))
    return songs


@router.get("")
async def get_songs(user: UserTable = Depends(current_user)) -> list[SSong]:
    songs = await SongRepository.find_all()
    # user_songs = list(filter(lambda x: x.user_id == user.id, songs))
    # if not user.is_superuser:
    #     public_songs = list(filter(lambda x: x.is_public == True, songs))
    #     if len(public_songs) > 0: user_songs.append(public_songs)
    return songs


@router.post("/tag")
async def add_song_tag(
        song_tag: Annotated[SSongTagAdd, Depends()],
        user: UserTable = Depends(current_user)
):
    song = await get_song_by_id(song_tag.song_id, user)
    if song.user_id == user.id:
        song_tag_id = await SongTagRepository.add_one(song_tag)
        return {'response': True, 'song_tag_id': song_tag_id}
    raise HTTPException(status_code=403)


@router.get("/tag/{id}")
async def get_song_tags(song_id: int, user: UserTable = Depends(current_user)) -> list[SSongTag]:
    song_tags = await SongTagRepository.find_by_song_id(song_id)
    return song_tags
