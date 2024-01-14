import datetime

from sqlalchemy import Date, ForeignKey, Integer, String, Boolean, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import expression

from core.models import Base

"""
"""


class AutoEventMail(Base):
    """
    name - название рассылки
    days_shift - рассылка будет сделана по мероприятиям, которые будут через заданное кол-во дней
    hours_shift - за заданное кол-во часов до старта
    minutes_shift -за заданное кол-во минут до старта
    * Времяар рассылки формирутеся из суммы всех временных сдвигов
    """

    # For automailing
    name: Mapped[str] = mapped_column(String(200), nullable=True, unique=False)
    days_shift: Mapped[int] = mapped_column(Integer(), nullable=True, unique=False)
    hours_shift: Mapped[int] = mapped_column(Integer(), nullable=True, unique=False)
    minutes_shift: Mapped[int] = mapped_column(Integer(), nullable=True, unique=False)
    archived: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=False, server_default=expression.false())

    # For manualmailing
    send_datetime: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=True, unique=False)
    send_now: Mapped[bool] = mapped_column(Boolean(), nullable=True, default=False, server_default=expression.false())

    # # ForeignKeys
    # region_id: Mapped[int] = mapped_column(ForeignKey("region.id"), nullable=True)
    #
    # # relationships
    # region = relationship("Region", back_populates="user")
    # role = relationship("UserRole", back_populates="user")
    # event = relationship("Event", back_populates="creator")
    # event_speaker = relationship("EventSpeaker", back_populates="speaker")
    # event_visitor = relationship("EventVisitor", back_populates="visitor")

# class HandMail(Base):
#     pass
