import datetime

from pydantic import BaseModel, ConfigDict, Field


class RoleBase(BaseModel):
    name: str = Field(max_length=100)
    archived: bool | None


class RoleCreate(RoleBase):
    pass


class RoleUpdatePartial(RoleBase):
    name: str | None = None
    archived: bool | None = None


class Role(RoleBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


# ....................UserRole...................

class UserRoleBase(BaseModel):
    user_id: int = Field()
    role_id: int = Field()


class UserRoleCreate(UserRoleBase):
    pass


class UserRoleUpdatePartial(UserRoleBase):
    user_id: int | None = None
    role_id: int | None = None


class UserRole(UserRoleBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
