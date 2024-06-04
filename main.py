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
import logging

from fastapi import FastAPI, APIRouter, Response, Request
from starlette.background import BackgroundTask
from fastapi.routing import APIRoute
from starlette.types import Message
from typing import Dict, Any
import logging


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



# logging.basicConfig(filename='info2.log', level=logging.DEBUG)
# async def log_info(req_body, res_body):
#     logging.info(req_body)
#     logging.info(res_body)
# async def set_body(request: Request, body: bytes):
#     async def receive() -> Message:
#         return {'type': 'http.request', 'body': body}
#     request._receive = receive
#
# @app.middleware('http')
# async def some_middleware(request: Request, call_next):
#     req_body = await request.body()
#     await set_body(request, req_body)  # not needed when using FastAPI>=0.108.0.
#     response = await call_next(request)
#
#     res_body = b''
#     async for chunk in response.body_iterator:
#         res_body += chunk
#
#     task = BackgroundTask(log_info, req_body, res_body)
#     return Response(content=res_body, status_code=response.status_code,
#                     headers=dict(response.headers), media_type=response.media_type, background=task)

app.include_router(albums_type_router)
app.include_router(country_router)
app.include_router(song_router)
app.include_router(user_router)
app.include_router(file_router)
app.include_router(interactions_router)

