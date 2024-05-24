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

class SSongTagAdd(BaseModel):
    song_id: int
    tag: str

class SSongTag(SSongTagAdd):
    id: int



# class SongTable(Model, DatedMixin):
#     __tablename__ = 'song'
#
#     id: Mapped[int] = mapped_column(primary_key=True)

