from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

from views.json.utils import to_camel


class ClothesBaseScheme(BaseModel):
    model_config = ConfigDict(from_attributes=True,
                              alias_generator=to_camel,
                              populate_by_name=True)


class ClothesScheme(ClothesBaseScheme):
    id: int
    title: str
    gender_id: int
    is_additional: bool
    additional_male: bool
    additional_female: bool
    value: str | None = None
    lora_files: list | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None
    clothes_type_id: int
