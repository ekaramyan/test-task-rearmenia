from typing import Generic, TypeVar
from pydantic import ConfigDict, BaseModel
from .utils import to_camel


T = TypeVar("T")


class UnifidedResponse(BaseModel, Generic[T]):

    is_success: bool = True
    message: str = ""
    data: T | None = None

    model_config = ConfigDict(from_attributes=True,
                              alias_generator=to_camel,
                              populate_by_name=True)
