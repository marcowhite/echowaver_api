from fastapi import APIRouter, HTTPException
from fastapi import Depends
from typing_extensions import Annotated

from database.models import UserTable
from repositories.album import AlbumTypeRepository, AlbumRepository
from routers.user import fastapi_users
from schemas.album import SAlbumTypeAdd, SAlbumType, SAlbumAdd, SAlbum

router = APIRouter(
    prefix='/albums',
    tags=['Albums']
)

current_user = fastapi_users.current_user()

@router.post("")
async def add_album(
        album: Annotated[SAlbumAdd, Depends()],
        user: UserTable = Depends(current_user)
    ):
    album_id = await AlbumRepository.add_one(album, user_id = user.id)
    return {'response': True, 'album_id': album_id}
@router.get("")
async def get_albums(user: UserTable = Depends(current_user)) -> list[SAlbum]:
    albums = await AlbumRepository.find_all()
    if not user.is_superuser:
        albums = list(filter(lambda x: x.is_public == True, albums))
    return albums

@router.post("/types")
async def add_album_type(
        album_type: Annotated[SAlbumTypeAdd, Depends()],
        user: UserTable = Depends(current_user)
    ):
    if user.is_superuser:
        album_type_id = await AlbumTypeRepository.add_one(album_type)
        return {'response': True, 'album_type_id': album_type_id}
    else:
        raise HTTPException(status_code=403, detail="Unauthorized")


@router.get("/types")
async def get_album_types() -> list[SAlbumType]:
    album_types = await AlbumTypeRepository.find_all()
    return album_types
