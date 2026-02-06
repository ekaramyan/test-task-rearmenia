from datetime import datetime

from pydantic import BaseModel, ConfigDict

from views.json.utils import to_camel


class ShoesBaseScheme(BaseModel):
    model_config = ConfigDict(from_attributes=True,
                              alias_generator=to_camel,
                              populate_by_name=True)


class ShoesScheme(ShoesBaseScheme):
    id: int
    title: str
    gender_id: int
    value: str
    lora_files: list | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None
