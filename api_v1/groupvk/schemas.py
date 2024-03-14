from pydantic import BaseModel, ConfigDict, Field


class GroupVKBase(BaseModel):
    name: str = Field(max_length=100)
    token: str = Field(max_length=500)


class GroupVKCreate(GroupVKBase):
    pass


class GroupVK(GroupVKBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
