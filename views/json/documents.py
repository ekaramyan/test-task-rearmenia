from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, HttpUrl

from database import Base

from .utils import to_camel


class DocumentBaseScheme(BaseModel):
    model_config = ConfigDict(from_attributes=True,
                              alias_generator=to_camel,
                              populate_by_name=True)
    


class DocumentCreate(BaseModel):
    title:str
    content:str


class Question(BaseModel):
    question: str


class DocumentResponse(DocumentBaseScheme):
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True