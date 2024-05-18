from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing_extensions import Optional

from . import Model
from .mixins.dated import DatedMixin

class AlbumTypeTable(Model):
    __tablename__ = 'album_types'

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str]


class AlbumTable(Model, DatedMixin):
    __tablename__ = 'albums'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    name: Mapped[str]
    description: Mapped[Optional[str]]
    public: Mapped[bool] = mapped_column(default=False)
    type: Mapped[int] = mapped_column(ForeignKey('album_types.id'))

    user = relationship("UserTable")