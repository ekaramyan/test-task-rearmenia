from pydantic import BaseModel, ConfigDict
from datetime import datetime

from views.json.utils import to_camel


class LoraForFaceBaseScheme(BaseModel):
    model_config = ConfigDict(from_attributes=True,
                              alias_generator=to_camel,
                              populate_by_name=True)


class LoraForFaceScheme(LoraForFaceBaseScheme):
    id: int
    face_id: str
    lora_name: str
    lora_file_path: str
    lora_img_url: str
    lora_gender_id: int
    model_appearances_id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None


class MixinLoraScheme(BaseModel):
    weight: str
    lora_file_path: str