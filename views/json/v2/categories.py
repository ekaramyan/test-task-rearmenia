from datetime import datetime

from pydantic import BaseModel, ConfigDict

from ..utils import to_camel


class CategoriesBaseScheme(BaseModel):
    model_config = ConfigDict(from_attributes=True,
                              alias_generator=to_camel,
                              populate_by_name=True)


class CategoriesScheme(CategoriesBaseScheme):
    id: int
    title: str
    number: int
    category_type_id: int
    note: str
    male: bool
    female: bool
    girl: bool
    boy: bool
    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None
