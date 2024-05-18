from fastapi import APIRouter
from fastapi import Depends
from typing_extensions import Annotated

from repository import SongRepository
from schemas import SSongAdd, SSong

router = APIRouter(
    prefix='/songs',
    tags=['Songs']
)


@router.post("")
async def add_song(
        song: Annotated[SSongAdd, Depends()]
):
    song_id = await SongRepository.add_one(song)
    return {'response': True, 'song_id': song_id}


@router.get("")
async def get_song() -> list[SSong]:
    songs = await SongRepository.find_all()
    return songs
