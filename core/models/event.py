import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base


class Event(Base):
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=False)
    description: Mapped[str] = mapped_column(Text(), nullable=True, unique=False)
    date_time: Mapped[datetime.datetime] = mapped_column(DateTime(), unique=False)

    region_id: Mapped[int] = mapped_column(ForeignKey("region.id"))
    # creator_id: Mapped[int] = mapped_column(ForeignKey("creator.id"))
    # speaker_id: Mapped[int] = mapped_column(ForeignKey("speaker.id"))

    # creator_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    # speaker_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)


    # relationships
    region = relationship("Region", back_populates="event")
    # creator = relationship("Creator", back_populates="event")
    # speaker = relationship("Speaker", back_populates="event")


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
