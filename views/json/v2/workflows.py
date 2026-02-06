from datetime import datetime

from pydantic import BaseModel, ConfigDict

from ..utils import to_camel


class WorkflowBaseScheme(BaseModel):
    model_config = ConfigDict(from_attributes=True,
                              alias_generator=to_camel,
                              populate_by_name=True)


class WorkflowScheme(WorkflowBaseScheme):
    id: int
    workflow_json: dict | None = None
    uploaded_by: str | None = None
    set_main_by: str | None = None
    is_main: bool
    description: str
    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None
