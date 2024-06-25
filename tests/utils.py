from dataclasses import dataclass
from datetime import datetime


@dataclass
class TestUserOk:
    __test__ = False
    vk_id: str = "1234554321"
    first_name: str = "1"
    last_name: str = "1"
    sex: int = 1
    city: str = "1"
    bdate: datetime.date = datetime.now().date()
    vk_group: str = "1"
    archived: bool = False


# vk_id: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
#
# first_name: Mapped[str] = mapped_column(String(100), nullable=True, unique=False)
# last_name: Mapped[str] = mapped_column(String(100), nullable=True, unique=False)
#
# sex: Mapped[int] = mapped_column(Integer(), nullable=True, unique=False)
# city: Mapped[str] = mapped_column(String(100), nullable=True, unique=False)
# bdate: Mapped[datetime.date] = mapped_column(Date(), nullable=True, unique=False)
#
# vk_group: Mapped[str] = mapped_column(String(100), nullable=True, unique=False)
#
# archived: Mapped[bool] = mapped_column(Boolean(), nullable=True, default=False)
