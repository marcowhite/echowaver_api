from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from . import Model
from .mixins.dated import DatedMixin


class LikedSongsTable(Model, DatedMixin):
    __tablename__ = "songs_likes"

    liker_id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)
    liked_id: Mapped[int] = mapped_column(ForeignKey('songs.id'), primary_key=True)


class RepostedSongsTable(Model, DatedMixin):
    __tablename__ = "songs_reposts"

    reposter_id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)
    reposted_id: Mapped[int] = mapped_column(ForeignKey('songs.id'), primary_key=True)


class LikedAlbumsTable(Model, DatedMixin):
    __tablename__ = "albums_likes"

    liker_id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)
    liked_id: Mapped[int] = mapped_column(ForeignKey('albums.id'), primary_key=True)


class RepostedAlbumsTable(Model, DatedMixin):
    __tablename__ = "albums_reposts"

    reposter_id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)
    reposted_id: Mapped[int] = mapped_column(ForeignKey('albums.id'), primary_key=True)
