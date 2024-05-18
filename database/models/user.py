from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import func
from datetime import datetime
from typing_extensions import Optional

from base import Model

class UserTable(Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    password: Mapped[str]
    display_name: Mapped[str]
    public: Mapped[bool] = mapped_column(default=False)
    type: Mapped[int] = relationship(foreign_keys='user_types.id')

    first_name: Mapped[Optional[str]]
    last_name: Mapped[Optional[str]]
    city: Mapped[Optional[str]]
    bio: Mapped[Optional[str]]

    url: Mapped[Optional[str]]
    avatar: Mapped[Optional[str]]
    background: Mapped[Optional[str]]

    created_at: Mapped[datetime] = mapped_column(default=func.now())

class UserTypeTable(Model):
    __tablename__ = 'user_types'

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str]
