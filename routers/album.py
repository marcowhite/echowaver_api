from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi import Depends
from typing_extensions import Annotated

from database.models import UserTable
from repositories.album import AlbumTypeRepository, AlbumRepository
from routers.file import upload_image
from routers.user import fastapi_users
from schemas.album import SAlbumTypeAdd, SAlbumType, SAlbumAdd, SAlbum

router = APIRouter(
    prefix='/album',
    tags=['Albums']
)

current_user = fastapi_users.current_user()


@router.post("")
async def add_album(
        album: Annotated[SAlbumAdd, Depends()],
        image_file: UploadFile = File(...),
        user: UserTable = Depends(current_user),
):
    try:
        image_responce = await upload_image(image_file)
    except Exception as e:
        raise e
    album_id = await AlbumRepository.add_one(album,cover_file=image_responce['message'], user_id=user.id)
    return {'response': True, 'album_id': album_id}


@router.get("")
async def get_albums(user: UserTable = Depends(current_user)) -> list[SAlbum]:
    albums = await AlbumRepository.find_all()
    if not user.is_superuser:
        albums = list(filter(lambda x: x.is_public == True, albums))
    return albums


@router.get("/{id}")
async def get_album_by_id(
        id: int,
        user: UserTable = Depends(current_user)
)-> SAlbum:
    album = await AlbumRepository.find_by_id(id)
    if album.is_public == True:
        return album
    else:
        if album.user_id == user.id:
            return album
        else:
            raise HTTPException(status_code=403, detail="Unauthorized")

@router.patch('/{id}')
async def update_album(
        id: int,
        album: Annotated[SAlbumAdd, Depends()],
        user: UserTable = Depends(current_user)
) -> SAlbum:
    selected_album = await AlbumRepository.find_by_id(id)
    if not selected_album:
        raise HTTPException(status_code=404, detail="Album not found")

    if user.id != selected_album.user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this album")

    updated_album = await AlbumRepository.update_by_id(id, album)
    if not updated_album:
        raise HTTPException(status_code=500, detail="Failed to update album")

    return updated_album


@router.delete("/{id}")
async def delete_album_by_id(
        id: int,
        user: UserTable = Depends(current_user)
):
    album = await get_album_by_id(id, user)
    if album.user_id == user.id:
        result = await AlbumRepository.delete_by_id(id)
        return {"responce": result}
    else:
        raise HTTPException(status_code=403, detail="Unauthorized")


@router.get("/user/{user_id}")
async def get_albums_by_user_id(
        user_id: int,
        user: UserTable = Depends(current_user)
) -> list[SAlbum]:
    albums = await AlbumRepository.find_all_by_user_id(user_id)
    if user.id != user_id:
        albums = list(filter(lambda x: x.is_public == True, albums))
    return albums


@router.post("/type")
async def add_album_type(
        album_type: Annotated[SAlbumTypeAdd, Depends()],
        user: UserTable = Depends(current_user)
):
    if user.is_superuser:
        album_type_id = await AlbumTypeRepository.add_one(album_type)
        return {'response': True, 'album_type_id': album_type_id}
    else:
        raise HTTPException(status_code=403, detail="Unauthorized")


@router.get("/type")
async def get_album_types(user: UserTable = Depends(current_user)) -> list[SAlbumType]:
    album_types = await AlbumTypeRepository.find_all()
    return album_types


@router.get("/type/{id}")
async def get_album_type_by_id(id: int,
                               user: UserTable = Depends(current_user)) -> SAlbumType:
    album_types = await AlbumTypeRepository.find_by_id(id)
    return album_types
