from sqlalchemy.dialects.postgresql import insert

from database.models import UserRoleTable, AlbumTypeTable
from database.connection import new_session

async def insert_default_rows():
    await insert_default_user_roles()
    await insert_default_album_types()


async def insert_default_user_roles():
    async with new_session() as session:
        await session.flush()
        query = insert(UserRoleTable).values(
            id=1,
            name="Fremium",
            permissions=None,
        ).on_conflict_do_nothing()
        await session.execute(query)

        query = insert(UserRoleTable).values(
            id=2,
            name="Premium",
            permissions="No limit, Ads free",
        ).on_conflict_do_nothing()
        await session.execute(query)

        await session.commit()
async def insert_default_album_types():
    async with new_session() as session:
        await session.flush()
        query = insert(AlbumTypeTable).values(
            id=1,
            type="Playlist",
        ).on_conflict_do_nothing()
        await session.execute(query)

        query = insert(AlbumTypeTable).values(
            id=2,
            type="Album",
        ).on_conflict_do_nothing()
        await session.execute(query)
        query = insert(AlbumTypeTable).values(
            id=3,
            type="EP",
        ).on_conflict_do_nothing()
        await session.execute(query)

        await session.commit()