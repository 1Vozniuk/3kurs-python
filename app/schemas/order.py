from pydantic import BaseModel, ConfigDict, Field


class OrderCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: int = Field(gt=0)
    status: str = Field(default="new", max_length=50)


class OrderOut(OrderCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
