from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

from views.json.utils import to_camel


class MainColorBaseScheme(BaseModel):
    model_config = ConfigDict(from_attributes=True,
                              alias_generator=to_camel,
                              populate_by_name=True)


class MainColorScheme(MainColorBaseScheme):
    id: int
    title: str
    value: str
    hex: str
    rgb: str
    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None
