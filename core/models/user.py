from sqlalchemy import Boolean, Date, String
from sqlalchemy.orm import Mapped, mapped_column  # relationship

from core.models import Base


class User(Base):
    vk_id: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    sex: Mapped[str] = mapped_column(Boolean(), nullable=True, unique=False)
    city: Mapped[str] = mapped_column(String(100), nullable=True, unique=False)
    bdate: Mapped[str] = mapped_column(Date(), unique=False)

    # region: Mapped[int] = mapped_column(ForeignKey("region.id"))

    # relationships
    # region = relationship("Region", back_populates="user")
