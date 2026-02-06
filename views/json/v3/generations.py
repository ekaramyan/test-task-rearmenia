from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from views.json.utils import to_camel


class GenerationBaseScheme(BaseModel):
    model_config = ConfigDict(from_attributes=True,
                              alias_generator=to_camel,
                              populate_by_name=True)


class GenerationScheme(GenerationBaseScheme):
    id: int
    id_gen_queue: str
    created_by: int
    load_date: datetime
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None


class GenerationFetchScheme(BaseModel):
    id_gen_queue: UUID

