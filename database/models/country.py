from sqlalchemy.orm import Mapped, mapped_column

from base import Model


class CountryTable(Model):
    __tablename__ = 'countries'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
