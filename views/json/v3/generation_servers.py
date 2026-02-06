from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime

from views.json.utils import to_camel


class GenerationServerBaseScheme(BaseModel):
    model_config = ConfigDict(from_attributes=True,
                              alias_generator=to_camel,
                              populate_by_name=True)

class GenerationServerCreateScheme(BaseModel):
    name: str
    socket: str


class GenerationServerUpdateScheme(BaseModel):
    name: Optional[str] = None
    socket: Optional[str] = None

class GenerationServerScheme(GenerationServerBaseScheme):
    id: int
    name: str
    socket: str
    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None

class GenerationServerStatsScheme(GenerationServerScheme):
    success: int
    none: int
    failed: int
