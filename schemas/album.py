from pydantic import BaseModel
from typing import Optional

class SAlbumTypeAdd(BaseModel):
    type: Optional[str] = None

class SAlbumType(SAlbumTypeAdd):
    id: int

class SAlbumAdd(BaseModel):
    name: str
    description: Optional[str] = None
    is_public: bool = False
    album_type_id: int = 1
    song_order: Optional[str] = None

class SAlbum(SAlbumAdd):
    cover_file: Optional[str] = None
    user_id: int
    id: int
