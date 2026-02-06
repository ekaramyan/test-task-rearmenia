from datetime import datetime

from pydantic import BaseModel, ConfigDict, HttpUrl, field_validator, Field

from ..utils import to_camel


class VideoBaseScheme(BaseModel):

    model_config = ConfigDict(from_attributes=True,
                              alias_generator=to_camel,
                              populate_by_name=True)


class VideoScheme(VideoBaseScheme):
    id: int

    video_url: str | None = None
    kling_url: str | None = None
    kling_task_id: str | None = None
    generation_ref: str
    generated_by: int
    status_id: int

    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None


class VideoArchiveInfoScheme(VideoBaseScheme):
    contract_uuid: str
    zip_url: str


class VideoGroupScheme(VideoBaseScheme):
    generation_ref: str
    created_at: datetime
    count: int
    generated_by: int
