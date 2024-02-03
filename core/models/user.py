from uuid import uuid4
from datetime import datetime, timedelta

from sqlalchemy import Date, ForeignKey, Integer, String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base

"""
VK API: https://dev.vk.com/ru/reference/objects/user

id: integer
username: No
first_name: string
last_name: string
sex: 1 — женский; 2 — мужской; 0 — пол не указан
city: object - {'id': 39, 'title': 'Владимир'}
bdate: string - '14.9.1970'

Дополнительная валидация полей будет на схемах
"""


class User(Base):
    vk_id: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    session: Mapped[str] = mapped_column(String(36), nullable=True, unique=True, default=str(uuid4()))
    session_expiration: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    first_name: Mapped[str] = mapped_column(String(100), nullable=True, unique=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=True, unique=False)

    sex: Mapped[int] = mapped_column(Integer(), nullable=True, unique=False)
    city: Mapped[str] = mapped_column(String(100), nullable=True, unique=False)
    bdate: Mapped[datetime.date] = mapped_column(Date(), nullable=True, unique=False)

    archived: Mapped[bool] = mapped_column(Boolean(), nullable=True, default=False)

    # ForeignKeys
    region_id: Mapped[int] = mapped_column(ForeignKey("region.id"), nullable=True)

    # relationships
    region = relationship("Region", back_populates="user")
    role = relationship("UserRole", back_populates="user")
    event = relationship("Event", back_populates="creator")
    event_speaker = relationship("EventSpeaker", back_populates="speaker")
    event_visitor = relationship("EventVisitor", back_populates="visitor")

    def __init__(self, *args, **kwargs):
        # Generate a unique session ID for each user during object creation
        if 'session_id' not in kwargs:
            kwargs['session_id'] = str(uuid4())

        super().__init__(*args, **kwargs)

    def refresh_session(self, expiration_minutes=30):
        # Update the session expiration timestamp
        self.session_expiration = datetime.utcnow() + timedelta(minutes=expiration_minutes)

    def is_session_expired(self):
        # Check if the session has expired
        return self.session_expiration is not None and self.session_expiration < datetime.utcnow()
