from sqlalchemy import ForeignKey, Column, Integer, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing_extensions import Optional

from . import Model
from .mixins.dated import DatedMixin


class UserTable(Model, DatedMixin):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    password: Mapped[str]
    display_name: Mapped[str]
    public: Mapped[bool] = mapped_column(default=False)
    type: Mapped[int] = mapped_column(ForeignKey('user_types.id'))

    first_name: Mapped[Optional[str]]
    last_name: Mapped[Optional[str]]
    city: Mapped[Optional[str]]
    bio: Mapped[Optional[str]]

    url: Mapped[Optional[str]]
    avatar: Mapped[Optional[str]]
    background: Mapped[Optional[str]]

    songs = relationship("SongTable", back_populates="user")
    albums = relationship("AlbumTable", back_populates="user")

    # followers = relationship(
    #     'UserTable', lambda: user_following,
    #     primaryjoin=lambda: UserTable.id == user_following.c.user_id,
    #     secondaryjoin=lambda: UserTable.id == user_following.c.following_id,
    #     backref='followers'
    # )


class UserTypeTable(Model):
    __tablename__ = 'user_types'

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str]

user_following = Table(
    'user_following', Model.metadata,
    Column('user_id', Integer, ForeignKey(UserTable.id), primary_key=True),
    Column('following_id', Integer, ForeignKey(UserTable.id), primary_key=True)
)