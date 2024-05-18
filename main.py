from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import create_tables,delete_tables
from router import router as songs_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    await create_tables()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(songs_router)


