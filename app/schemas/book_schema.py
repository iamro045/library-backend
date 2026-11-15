
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class BookCreate(BaseModel):

    book_id: str = Field(..., min_length=1, max_length=50)
    title: str = Field(..., min_length=2, max_length=200)
    author: str = Field(..., min_length=1, max_length=200)

    publication: Optional[str] = None
    price: Optional[float] = Field(default=None, ge=0)
    barcode: str = Field(..., min_length=1, max_length=100)

    model_config = ConfigDict(
        str_strip_whitespace=True
    )


class BookUpdate(BaseModel):

    title: Optional[str] = Field(default=None, min_length=2, max_length=200)
    author: Optional[str] = Field(default=None, min_length=1, max_length=200)

    publication: Optional[str] = None
    price: Optional[float] = Field(default=None, ge=0)
    barcode: Optional[str] = Field(default=None, min_length=1, max_length=100)

    model_config = ConfigDict(
        str_strip_whitespace=True
    )
