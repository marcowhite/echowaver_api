from fastapi import APIRouter
from fastapi import Depends
from typing_extensions import Annotated

from repositories.song import SongTagRepository
from schemas.song import SSongTagsAdd, SSongsTags


router = APIRouter(
    prefix='/songs',
    tags=['songs']
)


@router.post("/tags")
async def add_album_type(
        album_type: Annotated[SSongTagsAdd, Depends()]
):
    album_type_id = await SongTagRepository.add_one(album_type)
    return {'response': True, 'album_type_id': album_type_id}


@router.get("/tags")
async def get_album_types() -> list[SSongsTags]:
    album_types = await SongTagRepository.find_all()
    return album_types
