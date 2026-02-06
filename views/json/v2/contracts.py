import uuid
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from ..utils import to_camel

from datetime import datetime
from pydantic import BaseModel, UUID4
from typing import Optional, Dict, Any, List

class ContractServer(BaseModel):
    id: int
    server_url: str
    title: str

class ContractBaseScheme(BaseModel):
    id: int
    params_json: Optional[Dict[str, Any]] = None
    generation_id: int
    environment_type_id: int
    workflow_json: Optional[Dict[str, Any]] = None
    parent_id: Optional[int] = None
    load_date: datetime
    main_photo_url: str
    status_id: int
    contract_uuid: UUID | None = None
    is_valid: bool | None = None
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True,
                              alias_generator=to_camel,
                              populate_by_name=True)


class ContractScheme(ContractBaseScheme):
    children: List["ContractScheme"] = []


class GeneratedContractScheme(ContractScheme):
    id: int
    generated_photo_url: str
    created_by: int
    status: str
    count: int
    generation_uuid: str
    server: ContractServer
