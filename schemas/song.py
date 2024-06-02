from pydantic import BaseModel
from typing import Optional

class SSongAdd(BaseModel):
    name: str
    description: Optional[str] = None
    genre: Optional[str] = None

    background: Optional[str] = None

    is_public: bool = False

class SSong(SSongAdd):
    cover_file: Optional[str] = None
    audio_file: Optional[str] = None
    user_id: int
    id: int
int
class SSongTagAdd(BaseModel):
    song_id: int
    tag: str

class SSongTag(SSongTagAdd):
    id: int

class SSongListenAdd(BaseModel):
    song_id: int
    origin_country_id: int = 178
    meta: Optional[str] = None

class SSongListen(SSongListenAdd):
    id: int
    user_id: int