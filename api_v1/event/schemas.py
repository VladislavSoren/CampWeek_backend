from datetime import datetime

from pydantic import BaseModel, ConfigDict


class EventBase(BaseModel):
    name: str
    link: str
    add_link: str
    date_time: datetime
    time_start: str
    time_end: str
    is_reg_needed: bool
    approved: bool
    description: str
    add_info: str
    notes: str
    region_id: int
    creator_id: int


class EventCreate(EventBase):
    pass


class Event(EventBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
