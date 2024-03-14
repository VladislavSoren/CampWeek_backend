from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from core.models import Base


class GroupVK(Base):
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    token: Mapped[str] = mapped_column(String(500), nullable=False, unique=True)
