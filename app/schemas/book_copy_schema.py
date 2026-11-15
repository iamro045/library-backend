
from typing import Literal
from pydantic import BaseModel, Field, ConfigDict


class BookCopyCreate(BaseModel):

    model_config = ConfigDict(
        str_strip_whitespace=True
    )

    book_id: str = Field(
        ...,
        min_length=24,
        max_length=24
    )

    barcode: str = Field(
        ...,
        min_length=3,
        max_length=50
    )

    status: Literal[
        "available",
        "issued",
        "lost",
        "damaged"
    ] = "available"

    shelf_location: str = Field(
        ...,
        min_length=1,
        max_length=100
    )
