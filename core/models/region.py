from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base


class Region(Base):
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    # relationships
    user = relationship("User", back_populates="region")
