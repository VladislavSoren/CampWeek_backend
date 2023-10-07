from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base


class Event(Base):
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=False)
    description: Mapped[str] = mapped_column(Text(), nullable=True, unique=False)
    date_time: Mapped[str] = mapped_column(DateTime(), unique=False)

    region_id: Mapped[int] = mapped_column(ForeignKey("region.id"))
    creator_id: Mapped[int] = mapped_column(ForeignKey("creator.id"))
    speaker_id: Mapped[int] = mapped_column(ForeignKey("speaker.id"))

    # relationships
    region = relationship("Region", back_populates="event")
    creator = relationship("Creator", back_populates="event")
    speaker = relationship("Speaker", back_populates="event")
