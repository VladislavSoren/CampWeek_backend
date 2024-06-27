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


@dataclass
class TestEventOk:
    __test__ = False
    name: str = "TestEventOk123"
    link: str = "1"
    add_link: str = "1"
    date_time: datetime = datetime.now()
    time_start: str = "12:00"

    time_end: str = "13:00"
    is_reg_needed: bool = True
    approved: bool = False
    description: str = "1"
    add_info: str = "1"

    notes: str = "1"
    roles: str = "1"
    region_id: int = 1
    creator_id: int = 1
