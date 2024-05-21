from fastapi import APIRouter
from fastapi import Depends
from typing_extensions import Annotated

from repositories.album import AlbumTypeRepository
from schemas.album import SAlbumTypeAdd, SAlbumType

router = APIRouter(
    prefix='/albums',
    tags=['Albums']
)


@router.post("/types")
async def add_album_type(
        album_type: Annotated[SAlbumTypeAdd, Depends()]
):
    album_type_id = await AlbumTypeRepository.add_one(album_type)
    return {'response': True, 'album_type_id': album_type_id}


@router.get("/types")
async def get_album_types() -> list[SAlbumType]:
    album_types = await AlbumTypeRepository.find_all()
    return album_types
