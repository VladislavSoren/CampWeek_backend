from datetime import datetime

from sqlalchemy import ForeignKey, String, Text, Integer, UniqueConstraint, Boolean, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship
import sqlalchemy as sa

from core.models import Base


class Event(Base):
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=False)

    link: Mapped[str] = mapped_column(String(200), nullable=True, unique=False)
    add_link: Mapped[str] = mapped_column(String(200), nullable=True, unique=False)

    date_time: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False, unique=False)
    time_start: Mapped[str] = mapped_column(String(5), nullable=False, unique=False)
    time_end: Mapped[str] = mapped_column(String(5), nullable=False, unique=False)

    is_reg_needed: Mapped[bool] = mapped_column(
        sa.Boolean,
        nullable=False,
        server_default=sa.sql.true()
    )
    approved: Mapped[bool] = mapped_column(
        sa.Boolean,
        nullable=False,
        server_default=sa.sql.false()
    )

    description: Mapped[str] = mapped_column(Text(), nullable=True, unique=False)
    add_info: Mapped[str] = mapped_column(Text(), nullable=True, unique=False)
    notes: Mapped[str] = mapped_column(Text(), nullable=True, unique=False)
    roles: Mapped[str] = mapped_column(Text(), nullable=True, unique=False)

    # "meetingSpeakerInfo": "Регалии спикера", # NO REALISATION (#SPEAK)

    region_id: Mapped[int] = mapped_column(ForeignKey("region.id"))
    creator_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    # roles_target_audience  # NO REALISATION (#SPEAK)

    # relationships
    region = relationship("Region", back_populates="event")
    creator = relationship("User", back_populates="event")
    speaker = relationship("EventSpeaker", back_populates="event")
    visitor = relationship("EventVisitor", back_populates="event")


class EventSpeaker(Base):
    event_id: Mapped[int] = mapped_column(ForeignKey("event.id"), nullable=True)
    speaker_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=True)

    # additional properties
    __table_args__ = (UniqueConstraint("event_id", "speaker_id", name="unique_event_speaker_unit"),)

    # relationships
    event = relationship("Event", back_populates="speaker")
    speaker = relationship("User", back_populates="event_speaker")


class EventVisitor(Base):
    event_id: Mapped[int] = mapped_column(ForeignKey("event.id"), nullable=True)
    visitor_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=True)

    # additional properties
    __table_args__ = (UniqueConstraint("event_id", "visitor_id", name="unique_event_visitor_unit"),)

    # relationships
    event = relationship("Event", back_populates="visitor")
    visitor = relationship("User", back_populates="event_visitor")


# class Address(Base):
#     __tablename__ = "address"
#     id = mapped_column(Integer, primary_key=True)
#     street = mapped_column(String)
#     city = mapped_column(String)
#     state = mapped_column(String)
#     zip = mapped_column(String)
#
#
# class Customer(Base):
#     __tablename__ = "customer"
#     id = mapped_column(Integer, primary_key=True)
#     name = mapped_column(String)
#
#     billing_address_id = mapped_column(Integer, ForeignKey("address.id"))
#     shipping_address_id = mapped_column(Integer, ForeignKey("address.id"))
#
#     billing_address = relationship("Address", foreign_keys=[billing_address_id])
#     shipping_address = relationship("Address", foreign_keys=[shipping_address_id])
