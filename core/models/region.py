from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base


class Region(Base):
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    archived: Mapped[bool] = mapped_column(Boolean(), nullable=True, default=False)

    # relationships
    user = relationship("User", back_populates="region")
    event = relationship("Event", back_populates="region")
