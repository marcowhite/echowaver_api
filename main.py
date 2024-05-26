from contextlib import asynccontextmanager

from fastapi import FastAPI

from database.connection import create_tables
from database.defaults import insert_default_rows

from routers.album import router as albums_type_router
from routers.country import router as country_router
from routers.song import router as song_router
from routers.upload import router as upload_router
from routers.user import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # await delete_tables()
    await create_tables()
    await insert_default_rows()
    yield


app = FastAPI(
    lifespan=lifespan,
    title="Echowaver API"
)

app.include_router(albums_type_router)
app.include_router(country_router)
app.include_router(song_router)
app.include_router(user_router)
app.include_router(upload_router)
