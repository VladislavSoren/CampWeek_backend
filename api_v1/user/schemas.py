import datetime

from pydantic import BaseModel, ConfigDict, Field


class UserBase(BaseModel):
    vk_id: str = Field(max_length=100)
    first_name: str | None = Field(max_length=100)
    last_name: str | None = Field(max_length=100)
    sex: int | None = Field(ge=0, le=2)
    city: str | None = Field(max_length=100)
    bdate: datetime.date | None
    region_id: int | None = Field(ge=0, default=None)
    archived: bool | None = Field(default=False)


class UserCreate(UserBase):
    pass


class UserUpdatePartial(UserBase):
    vk_id: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    sex: int | None = None
    city: str | None = None
    bdate: datetime.date | None = None
    region_id: int | None = None
    archived: bool | None = None


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
