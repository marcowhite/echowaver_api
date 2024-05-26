from pydantic import BaseModel
from typing import Optional


class SSongLikeAdd(BaseModel):
    liked_id: int


class SSongLike(SSongLikeAdd):
    liker_id: int


class SSongRepostAdd(BaseModel):
    liked_id: int


class SSongRepost(SSongRepostAdd):
    liker_id: int


class SAlbumLikeAdd(BaseModel):
    liked_id: int


class SAlbumLike(SAlbumLikeAdd):
    liker_id: int


class SAlbumRepostAdd(BaseModel):
    liked_id: int


class SAlbumRepost(SAlbumRepostAdd):
    liker_id: int
