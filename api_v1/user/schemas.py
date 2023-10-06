from pydantic import BaseModel, ConfigDict


class AutoBase(BaseModel):
    brand: str
    park_id: int


class AutoCreate(AutoBase):
    pass


class Auto(AutoBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
