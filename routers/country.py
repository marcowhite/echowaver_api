from fastapi import APIRouter, HTTPException
from fastapi import Depends
from typing_extensions import Annotated

from database.models import UserTable
from repositories.country import CountryRepository
from routers.user import fastapi_users
from schemas.country import SCountryAdd, SCountry

router = APIRouter(
    prefix='/countries',
    tags=['Countries']
)

current_user = fastapi_users.current_user()


@router.post("")
async def add_country(
        country: Annotated[SCountryAdd, Depends()],
        user: UserTable = Depends(current_user)
):
    if user.is_superuser:
        country_id = await CountryRepository.add_one(country)
        return {'response': True, 'country_id': country_id}
    else:
        raise HTTPException(status_code=403, detail="Unauthorized")


@router.get("")
async def get_countries() -> list[SCountry]:
    countries = await CountryRepository.find_all()
    return countries
