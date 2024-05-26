from sqlalchemy import select

from database.connection import new_session
from database.models.country import CountryTable
from schemas.country import SCountryAdd, SCountry

from fastapi.encoders import jsonable_encoder


class CountryRepository:
    @classmethod
    async def add_one(cls, data: SCountryAdd) -> int:
        async with new_session() as session:
            country_dict = data.model_dump()
            print(country_dict)
            country = CountryTable(**country_dict)
            session.add(country)
            await session.flush()
            await session.commit()
            return country.id

    @classmethod
    async def find_by_id(cls, id: int) -> SCountry:
        async with new_session() as session:
            query = select(CountryTable).filter(CountryTable.id == id)
            result = await session.execute(query)
            country_model = result.scalars().first()
            country_shema = SCountry.model_validate(jsonable_encoder(country_model))
            return country_shema

    @classmethod
    async def find_all(cls) -> list[SCountry]:
        async with new_session() as session:
            query = select(CountryTable)
            result = await session.execute(query)
            country_models = result.scalars().all()
            country_shemas = [SCountry.model_validate(jsonable_encoder(country_model)) for country_model in
                              country_models]
            return country_shemas
