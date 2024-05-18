from pydantic import BaseModel
from typing import Optional

class SSongAdd(BaseModel):
    name: str
    description: Optional[str] = None
    genre: Optional[str] = None
    public: bool = False

class SSong(SSongAdd):
    id: int


class SAlbumTypeAdd(BaseModel):
    type: Optional[str] = None

class SAlbumType(SAlbumTypeAdd):
    id: int