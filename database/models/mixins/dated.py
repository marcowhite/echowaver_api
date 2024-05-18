from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func
from datetime import datetime
from typing_extensions import Optional


class DatedMixin:
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())
