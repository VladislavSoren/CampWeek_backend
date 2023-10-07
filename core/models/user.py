from sqlalchemy import Boolean, Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base

"""
VK API: https://dev.vk.com/ru/reference/objects/user

id: integer
username: No
first_name: string
last_name: string
sex: 1 — женский; 2 — мужской; 0 — пол не указан
city:

bdate:
"""


class User(Base):
    vk_id: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    first_name: Mapped[str] = mapped_column(String(100), nullable=True, unique=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=True, unique=False)

    sex: Mapped[str] = mapped_column(Boolean(), nullable=True, unique=False)
    city: Mapped[str] = mapped_column(String(100), nullable=True, unique=False)
    bdate: Mapped[str] = mapped_column(Date(), nullable=True, unique=False)

    region_id: Mapped[int] = mapped_column(ForeignKey("region.id"))

    # relationships
    region = relationship("Region", back_populates="user")
    # event_creator = relationship("Event", back_populates="creator")
    # event_speaker = relationship("Event", back_populates="speaker")


# class Admin(Base):
#     user: Mapped[int] = mapped_column(ForeignKey("user.id"), unique=True)
#
#
# class Creator(Base):
#     user: Mapped[int] = mapped_column(ForeignKey("user.id"), unique=True)
#
#
# class Speaker(Base):
#     user: Mapped[int] = mapped_column(ForeignKey("user.id"), unique=True)
