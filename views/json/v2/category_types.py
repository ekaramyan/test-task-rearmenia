from datetime import datetime

from pydantic import BaseModel, ConfigDict

from ..utils import to_camel


class CategoryTypeBaseScheme(BaseModel):
    model_config = ConfigDict(from_attributes=True,
                              alias_generator=to_camel,
                              populate_by_name=True)


class CategoryTypeScheme(CategoryTypeBaseScheme):
    id: int
    title: str
    value: str
    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None
