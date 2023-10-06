from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base


class ParkOwner(Base):
    name: Mapped[str] = mapped_column(String(100), unique=False)

    # relationships
    park = relationship("Park", back_populates="parkowner")
