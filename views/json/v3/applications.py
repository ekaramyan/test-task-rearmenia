import os.path
from typing import Optional

from pydantic import BaseModel, Field, field_validator, model_validator

from config import BASE_DIR


class Base64File(BaseModel):
    filename: str
    data: str


class Environment(BaseModel):
    environment_place: str


class OtherEnvironmentType(BaseModel):
    environment_lightning: Optional[str] = Field(default="sunny")
    count: int = Field(default=7)
    name: str = Field(default="other")
    data: list[Environment]

    @field_validator(
        'environment_lightning',
        'count',
        mode='before',
    )
    @classmethod
    def empty_string_to_none(cls, v):
        return v if v not in ("", None) else None

    @model_validator(mode='after')
    def set_defaults(self):
        defaults = {
            "environment_lightning": "sunny",
            "count": 7,
        }

        for field, value in defaults.items():
            if getattr(self, field) is None:
                setattr(self, field, value)

        return self


class StudioEnvironmentType(BaseModel):
    name: str = Field(default="studio")
    count: int = Field(default=5)
    background_color: str = Field(default="white")
    environment_lightning: Optional[str] = Field(default="studio")
    data: list[Environment]

    @field_validator(
        'environment_lightning',
        'count',
        mode='before',
    )
    @classmethod
    def empty_string_to_none(cls, v):
        return v if v not in ("", None) else None

    @model_validator(mode='after')
    def set_defaults(self):
        defaults = {
            "environment_lightning": "studio",
            "count": 5,
        }

        for field, value in defaults.items():
            if getattr(self, field) is None:
                setattr(self, field, value)

        return self

    def model_dump(self, *args, **kwargs):
        exclude = kwargs.pop("exclude", set())
        if isinstance(exclude, dict):
            exclude["background_color"] = ...
        else:
            exclude = set(exclude)
            exclude.add("background_color")

        return super().model_dump(*args, exclude=exclude, **kwargs)


class EnvironmentsModel(BaseModel):
    data: list[StudioEnvironmentType | OtherEnvironmentType] = Field(
        default=[
            StudioEnvironmentType(data=[Environment(environment_place="studio")]),
            OtherEnvironmentType(data=[Environment(environment_place="city_park")]),
        ]
    )


class AdditionalClothes(BaseModel):
    lora_file_path: str | None = Field(default=None)
    value: str | None = Field(default="")

    @model_validator(mode='after')
    def set_defaults(self):
        if self.lora_file_path is None:
            self.lora_file_path = "Add_clothes_LoRA/Woman/lower/w1trousers-000006.safetensors"
        if self.value is None:
            self.value = ""
        return self


class Shoes(AdditionalClothes):
    lora_file_path: str | None = Field(default=None)
    value: str | None = Field(default="")

    @model_validator(mode='after')
    def set_defaults(self):
        if self.lora_file_path is None:
            self.lora_file_path = "Add_shoes_LoRA/Shoes_LoRA/Man_Shoes_LoRA/m1kr0ss-000006.safetensors"
        if self.value is None:
            self.value = ""
        return self


class AddAppRequestScheme(BaseModel):
    product_type: Optional[str] = None
    clothes_gender: Optional[str] = None
    clothes_main_category: Optional[str] = None
    clothes_add_category: Optional[AdditionalClothes] = None
    clothes_add_color: Optional[str] = None
    clothes_add_material: Optional[str] = None
    add_clothes_category: Optional[Shoes] = Field(default=None, serialization_alias="shoes")
    add_clothes_color: Optional[str] = Field(default=None, serialization_alias="shoes_color")
    model_face: Optional[str] = None
    face_id: Optional[str] = None
    model_appearance: Optional[str] = None
    model_age: Optional[str] = None
    model_physique: Optional[str] = None
    model_hair_color: Optional[str] = None
    model_hair_length: Optional[str] = None
    model_pose: Optional[str] = None
    environments: EnvironmentsModel
    image_ratio: Optional[str] = None
    photo_extension: Optional[str] = None
    files: list[Base64File]
    generation_server_url: Optional[str] = None
    workflow_id: Optional[int] = None

    @field_validator(
        'product_type', 'clothes_gender',
        "face_id",
        "generation_server_url",
        'clothes_main_category', 'clothes_add_category',
        'clothes_add_color', 'clothes_add_material',
        'add_clothes_category', 'add_clothes_color',
        'model_face', 'model_appearance', 'model_age',
        'model_physique', 'model_hair_color', 'model_hair_length',
        'model_pose', 'image_ratio', 'photo_extension',
        mode='before',
    )
    @classmethod
    def empty_string_to_none(cls, v):
        return v if v not in ("", None) else None

    @model_validator(mode='after')
    def set_defaults(self):
        defaults = {
            "product_type": "clothes",
            "clothes_gender": "man",
            "clothes_main_category": "tshirt",
            "clothes_add_category": AdditionalClothes(
                value="",
                lora_file_path="Lea_Seydoux_V3.safetensors"
            ),
            "clothes_add_color": "",
            "clothes_add_material": "",
            "add_clothes_category": Shoes(
                value="",
                lora_file_path="Lea_Seydoux_V3.safetensors"
            ),
            "add_clothes_color": "",

            "model_face": "Faces/Man_fp8/EU_Aleks_1152r16fp8s1120_2025-05-26.safetensors" if self.clothes_gender == "man"
            else "Faces/Woman_fp8/EU_Elena_1152r16fp8s1080_2025-05-22.safetensors",
            "face_id": "",
            "model_appearance": "european",
            "model_age": "35",
            "model_physique": "sports",
            "model_hair_color": "blonde",
            "model_hair_length": "short",
            "generation_server_url": "http://192.144.167.54:8188",
            "model_pose": os.path.join(BASE_DIR, "storage", "poses", "man", "istockphoto-916449556-2048x2048.jpg"),
            "image_ratio": "16:9",
            "photo_extension": "jpg"
        }

        for field, value in defaults.items():
            if getattr(self, field) is None:
                setattr(self, field, value)

        return self
