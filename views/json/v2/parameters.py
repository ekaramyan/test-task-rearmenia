from datetime import datetime

from pydantic import BaseModel, ConfigDict

from ..utils import to_camel


class ParameterBaseScheme(BaseModel):
    model_config = ConfigDict(from_attributes=True,
                              alias_generator=to_camel,
                              populate_by_name=True)


class ParameterScheme(ParameterBaseScheme):
    id: int
    category: str
    product_type:str
    model_face:str
    model_physique:str
    model_age:str
    model_appearance:str
    model_hair_color:str
    model_hair_length:str
    model_pose:str
    environment:str
    lighting:str
    rotation:str
    output_extension:str
    gender:str

    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None
