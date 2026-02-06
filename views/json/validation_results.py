from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict
from .utils import to_camel


class ValidationResultBaseScheme(BaseModel):

    model_config = ConfigDict(from_attributes=True,
                              alias_generator=to_camel,
                              populate_by_name=True)


class ValidationResultScheme(ValidationResultBaseScheme):

    is_valid: bool
    validation_error: Optional[str]
