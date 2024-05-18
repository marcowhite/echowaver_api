from contextlib import asynccontextmanager
from fastapi import FastAPI
from database.connection import create_tables,delete_tables
from routers.album import router as albums_type_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    await create_tables()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(albums_type_router)


