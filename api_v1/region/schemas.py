from pydantic import BaseModel, ConfigDict, Field


class RegionBase(BaseModel):
    name: str = Field(max_length=100)
    archived: bool | None = False


class RegionCreate(RegionBase):
    pass


class RegionUpdatePartial(RegionBase):
    name: str | None = None
    archived: bool | None = None


class Region(RegionBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
