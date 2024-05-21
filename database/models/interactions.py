from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from . import Model
from .mixins.dated import DatedMixin


class LikedSongsTable(Model, DatedMixin):
    __tablename__ = "song_like"

    liker_id: Mapped[int] = mapped_column(ForeignKey('user.id'), primary_key=True)
    liked_id: Mapped[int] = mapped_column(ForeignKey('song.id'), primary_key=True)


class RepostedSongsTable(Model, DatedMixin):
    __tablename__ = "song_repost"

    reposter_id: Mapped[int] = mapped_column(ForeignKey('user.id'), primary_key=True)
    reposted_id: Mapped[int] = mapped_column(ForeignKey('song.id'), primary_key=True)


class LikedAlbumsTable(Model, DatedMixin):
    __tablename__ = "album_like"

    liker_id: Mapped[int] = mapped_column(ForeignKey('user.id'), primary_key=True)
    liked_id: Mapped[int] = mapped_column(ForeignKey('album.id'), primary_key=True)


class RepostedAlbumsTable(Model, DatedMixin):
    __tablename__ = "album_repost"

    reposter_id: Mapped[int] = mapped_column(ForeignKey('user.id'), primary_key=True)
    reposted_id: Mapped[int] = mapped_column(ForeignKey('album.id'), primary_key=True)
