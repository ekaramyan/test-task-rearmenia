from datetime import datetime
from pydantic import BaseModel, ConfigDict
from .utils import to_camel


class RoleBaseScheme(BaseModel):

    model_config = ConfigDict(from_attributes=True,
                              alias_generator=to_camel,
                              populate_by_name=True)


class RoleScheme(RoleBaseScheme):

    id: int

    name: str
    role_value: int | None = None

    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None


class RoleCreateScheme(RoleBaseScheme):

    name: str
    role_value: int


class RoleUpdateScheme(RoleBaseScheme):

    name: str | None = None
    role_value: int | None = None
