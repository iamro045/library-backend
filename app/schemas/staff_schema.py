
from pydantic import BaseModel, Field, ConfigDict
from typing import Literal


class StaffCreate(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8, max_length=128)
    role: Literal["admin", "librarian"] = "librarian"

    model_config = ConfigDict(str_strip_whitespace=True)


class StaffLogin(BaseModel):
    username: str
    password: str


class StaffUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=2, max_length=100)
    role: Literal["admin", "librarian"] | None = None
    is_active: bool | None = None

    model_config = ConfigDict(str_strip_whitespace=True)


class StaffResponse(BaseModel):
    staff_id: str
    full_name: str
    username: str
    role: str
    is_active: bool
