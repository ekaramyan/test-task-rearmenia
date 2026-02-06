from datetime import datetime

from pydantic import BaseModel, ConfigDict

from views.json.utils import to_camel


class MaterialBaseScheme(BaseModel):
    model_config = ConfigDict(from_attributes=True,
                              alias_generator=to_camel,
                              populate_by_name=True)


class MaterialScheme(MaterialBaseScheme):
    id: int
    title: str
    value: str
    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None
