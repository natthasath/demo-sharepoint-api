from fastapi import Form
from pydantic import BaseModel, Field, EmailStr, SecretStr
from typing import List, Union
import inspect

def form_body(cls):
    cls.__signature__ = cls.__signature__.replace(
        parameters=[
            arg.replace(default=Form(default = arg.default) if arg.default is not inspect._empty else Form(...))
            for arg in cls.__signature__.parameters.values()
        ]
    )
    return cls

@form_body
class ConfigSchema(BaseModel):
    username: EmailStr = Field(...)
    password: SecretStr = Field(...)
    site_name: str = Field(...)
    list_name: str = Field(...)
    folder_name: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "username": "username@nida.ac.th",
                "password": "password",
                "site_name": "site name",
                "list_name": "list name",
                "folder_name": "folder name"
            }
        }

@form_body
class SearchSchema(BaseModel):
    record_id: int = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "record_id": "1"
            }
        }

@form_body
class CreateSchema(BaseModel):
    columns: str = Field(...)
    rows: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "column": "[Title, Name]",
                "rows": "[TH, Thailand]"
            }
        }