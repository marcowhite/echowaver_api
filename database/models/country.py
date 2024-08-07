from sqlalchemy.orm import Mapped, mapped_column

from . import Model


class CountryTable(Model):
    __tablename__ = 'country'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    code: Mapped[str]
