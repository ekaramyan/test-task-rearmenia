from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, field_validator
from .utils import to_camel
from .roles import RoleScheme


class UserBaseScheme(BaseModel):

    model_config = ConfigDict(from_attributes=True,
                              alias_generator=to_camel,
                              populate_by_name=True)


class UserScheme(UserBaseScheme):

    id: int
    role: RoleScheme
    photo: str | None = None
    first_name: str
    last_name: str
    email: EmailStr
    login: str
    phone: str | None = None
    tg: str | None = None

    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None


class UserShortScheme(UserBaseScheme):
    id: int
    role_id: int | None = None
    photo: str | None = None
    first_name: str
    last_name: str
    login: str
    email: EmailStr
    phone: str | None = None
    tg: str | None = None


class UserCreateScheme(UserBaseScheme):

    password: str
    role_id: int
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    login: str
    phone: str | None = None
    tg: str | None = None

class UserUpdateScheme(UserBaseScheme):

    password: str | None = None
    role_id: int | None = None
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    login: str | None = None
    phone: str | None = None
    tg: str | None = None
