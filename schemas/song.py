from pydantic import BaseModel
from typing import Optional

class SSongAdd(BaseModel):
    path: str

    name: str
    description: Optional[str] = None
    genre: Optional[str] = None
    public: bool = False
    background: Optional[str] = None
    cover: Optional[str] = None

class SSong(SSongAdd):
    id: int

class SSongTagsAdd(BaseModel):
    song_id: int
    tag: str

class SSongsTags(SSongTagsAdd):
    id: int