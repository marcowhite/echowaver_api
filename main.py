from contextlib import asynccontextmanager
from fastapi import FastAPI
from database.connection import create_tables, delete_tables

from routers.album import router as albums_type_router
from routers.country import router as country_router
from routers.song import router as song_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    await create_tables()
    yield


app = FastAPI(
    lifespan=lifespan,
    title="Echowaver API"
)
app.include_router(albums_type_router)
app.include_router(country_router)
app.include_router(song_router)
