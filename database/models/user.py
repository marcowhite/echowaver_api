from sqlalchemy import ForeignKey, Column, Integer, Table, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing_extensions import Optional

from . import Model
from .mixins.dated import DatedMixin

from fastapi_users.db import SQLAlchemyBaseUserTable


class UserRoleTable(Model):
    __tablename__ = 'user_role'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    permissions: Mapped[Optional[str]]


class UserTable(SQLAlchemyBaseUserTable[int], Model, DatedMixin):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)

    email: Mapped[str] = mapped_column(String(length=320), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(default=False, nullable=False)

    is_public: Mapped[bool] = mapped_column(default=True, nullable=False)

    role_id: Mapped[int] = mapped_column(ForeignKey('user_role.id'))

    display_name: Mapped[str]
    first_name: Mapped[Optional[str]]
    last_name: Mapped[Optional[str]]
    city: Mapped[Optional[str]]
    bio: Mapped[Optional[str]]

    url: Mapped[Optional[str]]
    avatar: Mapped[Optional[str]]
    background: Mapped[Optional[str]]
    spotlight: Mapped[Optional[JSONB]] = mapped_column(type_=JSONB)
    # followers = relationship(
    #     'UserTable', lambda: user_following,
    #     primaryjoin=lambda: UserTable.id == user_following.c.user_id,
    #     secondaryjoin=lambda: UserTable.id == user_following.c.following_id,
    #     backref='followers'
    # )
    followers = relationship(
        'UserFollowTable',
        foreign_keys='UserFollowTable.following_id',
        back_populates='following_user'
    )

    followings = relationship(
        'UserFollowTable',
        foreign_keys='UserFollowTable.user_id',
        back_populates='user'
    )

class UserFollowTable(Model):
    __tablename__ = 'user_following'

    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), primary_key=True)
    following_id: Mapped[int] = mapped_column(ForeignKey('user.id'), primary_key=True)

    user = relationship('UserTable', foreign_keys=[user_id], back_populates='followings')
    following_user = relationship('UserTable', foreign_keys=[following_id], back_populates='followers')
# user_following = Table(
#     'user_following', Model.metadata,
#     Column('user_id', Integer, ForeignKey(UserTable.id), primary_key=True),
#     Column('following_id', Integer, ForeignKey(UserTable.id), primary_key=True)
# )
