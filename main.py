from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.connection import create_tables
from database.defaults import insert_default_rows

from routers.album import router as albums_type_router
from routers.country import router as country_router
from routers.song import router as song_router
from routers.file import router as file_router
from routers.user import router as user_router
from routers.interaction import router as interactions_router
from routers.stream import router as websocket_router


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

origins = [
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)

app.include_router(albums_type_router)
app.include_router(country_router)
app.include_router(song_router)
app.include_router(user_router)
app.include_router(file_router)
app.include_router(interactions_router)
