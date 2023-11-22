import datetime

from pydantic import BaseModel, ConfigDict, Field


class EventVisitorBase(BaseModel):
    event_id: int = Field()
    visitor_id: int = Field()


class EventVisitorCreate(EventVisitorBase):
    pass


class EventVisitorUpdatePartial(EventVisitorBase):
    event_id: int | None = None
    visitor_id: int | None = None


class EventVisitor(EventVisitorBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
