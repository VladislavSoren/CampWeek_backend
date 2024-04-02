from datetime import datetime

from pydantic import BaseModel, ConfigDict


class EventBase(BaseModel):
    name: str
    link: str
    add_link: str
    date_time: datetime
    time_start: str = "20:00"
    time_end: str = "21:00"
    is_reg_needed: bool = True
    approved: bool = False
    description: str
    add_info: str
    notes: str
    roles: str
    region_id: int
    creator_id: int


class EventCreate(EventBase):
    pass


class EventUpdatePartial(EventBase):
    name: str | None = None
    link: str | None = None
    add_link: str | None = None
    date_time: datetime | None = None
    time_start: str | None = None
    time_end: str | None = None
    is_reg_needed: bool | None = None
    approved: bool | None = None
    description: str | None = None
    add_info: str | None = None
    notes: str | None = None
    roles: str | None = None
    region_id: int | None = None
    creator_id: int | None = None


class Event(EventBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
