from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from views.json.generated import SourceItem
from .utils import to_camel


class QueueBaseScheme(BaseModel):
    model_config = ConfigDict(from_attributes=True,
                              alias_generator=to_camel,
                              populate_by_name=True)


class QueueScheme(QueueBaseScheme):
    id: int
    photo_url: Optional[str] | None = None
    source_data: Optional[List[SourceItem]] | None = None
    params: Optional[List[str]] | None = None
    queue_position: Optional[int] | None = None

    loaded_at: datetime | None = None
    generated_by: Optional[str] | None = None

    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None
