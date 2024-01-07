import datetime

from pydantic import BaseModel, ConfigDict, Field


class AutoEventMailBase(BaseModel):
    name: str = Field(max_length=200)
    days_shift: int | None = Field(ge=0, default=None)
    hours_shift: int | None = Field(ge=0, le=24, default=None)
    minutes_shift: int | None = Field(ge=0, le=60, default=None)
    archived: bool | None = Field(default=False)


class AutoEventMailCreate(AutoEventMailBase):
    pass


class AutoEventMailUpdatePartial(AutoEventMailBase):
    name: str | None = None
    days_shift: int | None = None
    hours_shift: int | None = None
    minutes_shift: int | None = None
    archived: bool | None = None


class AutoEventMail(AutoEventMailBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
