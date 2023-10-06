from pydantic import BaseModel, ConfigDict


class DriverBase(BaseModel):
    name: str


class DriverCreate(DriverBase):
    pass


class Driver(DriverBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
