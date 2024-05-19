from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing_extensions import Optional

from . import Model
from .mixins.dated import DatedMixin


class SongTable(Model, DatedMixin):
    __tablename__ = 'songs'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    path: Mapped[str]

    name: Mapped[str]
    description: Mapped[Optional[str]]
    genre: Mapped[Optional[str]]
    public: Mapped[bool] = mapped_column(default=False)
    background: Mapped[str]
    cover: Mapped[str]

    user = relationship("UserTable", back_populates="songs")
    listenings = relationship("ListeningTable", back_populates='song')
    tags = relationship("TagsTable", back_populates='song')

class ListeningTable(Model, DatedMixin):
    __tablename__ = 'listenings'

    id: Mapped[int] = mapped_column(primary_key=True)
    song_id: Mapped[int] = mapped_column(ForeignKey('songs.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    origin_country_id: Mapped[int] = mapped_column(ForeignKey('countries.id'))
    meta: Mapped[Optional[str]]

    song = relationship("SongTable",back_populates='listenings')

class TagsTable(Model):
    __tablename__ = 'songs_tags'
    id: Mapped[int] = mapped_column(primary_key=True)
    song_id: Mapped[int] = mapped_column(ForeignKey('songs.id'))
    tag: Mapped[str]

    song = relationship("SongTable", back_populates='tags')