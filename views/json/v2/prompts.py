from datetime import datetime

from pydantic import BaseModel, ConfigDict

from ..utils import to_camel


class PromptBaseScheme(BaseModel):
    model_config = ConfigDict(from_attributes=True,
                              alias_generator=to_camel,
                              populate_by_name=True)


class PromptScheme(PromptBaseScheme):
    id: int
    prompt_id: str
    load_date: datetime
    generation_date: datetime
    generated_by: int
    workflow_id: int
    parameters_json: str
    input_img_url: str
    output_image_url: str
    contract_id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None
