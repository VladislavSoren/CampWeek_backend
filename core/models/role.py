
from sqlalchemy import ForeignKey, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base


class Role(Base):
    name: Mapped[str] = mapped_column(String(100), nullable=True, unique=True)
    archived: Mapped[bool] = mapped_column(Boolean(), nullable=True, default=False)

    # relationships
    user = relationship("UserRole", back_populates="role")


class UserRole(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("role.id"), nullable=True)

    # relationships
    user = relationship("User", back_populates="role")
    role = relationship("Role", back_populates="user")
