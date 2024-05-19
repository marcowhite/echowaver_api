from pydantic import BaseModel
from typing import Optional

class SAlbumTypeAdd(BaseModel):
    type: Optional[str] = None

class SAlbumType(SAlbumTypeAdd):
    id: int