import datetime

from pydantic import BaseModel, ConfigDict, Field


class UserBase(BaseModel):
    vk_id: int = Field(ge=0)
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    sex: int = Field(ge=0, le=2)
    city: str = Field(max_length=100)
    bdate: datetime.date
    region_id: int = Field(ge=0, default=1)


class UserCreate(UserBase):
    pass


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
