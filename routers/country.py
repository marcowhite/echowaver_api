from fastapi import APIRouter
from fastapi import Depends
from typing_extensions import Annotated

from repositories.album import AlbumTypeRepository
from schemas.country import SCountryAdd, SCountry

router = APIRouter(
    prefix='/countries',
    tags=['Countries']
)


@router.post("")
async def add_country(
        country: Annotated[SCountryAdd, Depends()]
):
    country_id = await AlbumTypeRepository.add_one(country)
    return {'response': True, 'country_id': country_id}


@router.get("")
async def get_countries() -> list[SCountry]:
    album_types = await AlbumTypeRepository.find_all()
    return album_types