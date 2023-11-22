import datetime

from pydantic import BaseModel, ConfigDict, Field


class EventSpeakerBase(BaseModel):
    event_id: int = Field()
    speaker_id: int = Field()


class EventSpeakerCreate(EventSpeakerBase):
    pass


class EventSpeakerUpdatePartial(EventSpeakerBase):
    event_id: int | None = None
    speaker_id: int | None = None


class EventSpeaker(EventSpeakerBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
