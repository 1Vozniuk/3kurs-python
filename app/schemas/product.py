from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    price: Decimal = Field(gt=0)
    category_id: int


class ProductOut(ProductCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
