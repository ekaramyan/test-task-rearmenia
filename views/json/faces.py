from datetime import datetime

from pydantic import BaseModel, ConfigDict

from .utils import to_camel


class FaceBaseScheme(BaseModel):
    model_config = ConfigDict(from_attributes=True,
                              alias_generator=to_camel,
                              populate_by_name=True)


class FaceScheme(FaceBaseScheme):
    id: int
    name: str
    link: str
