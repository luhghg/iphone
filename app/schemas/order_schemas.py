from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from typing import Literal



class OrderItemCreate(BaseModel):
    order_id: int
    product_variant_id: int
    quantity: int
    price_at_purchase : float





    
class OrderItemResponse(BaseModel):
    id: int
    product_variant_id: int
    quantity: int
    price_at_purchase: float

    model_config = ConfigDict(from_attributes=True)


class OrderBase(BaseModel):
    pass

class OrderCreate(OrderBase):
    delivery_address: str


class OrderStatusUpdate(OrderBase):
    status: Literal["pending", "paid", "shipped", "delivered", "cancelled"] 



class OrderResponse(OrderBase):
    id: int
    user_id: int
    status: Literal["pending", "paid", "shipped", "delivered", "cancelled"] = Field(default="pending")
    total_price: float
    delivery_address: str
    items: list[OrderItemResponse]
    created_at: datetime 

    model_config = ConfigDict(from_attributes=True)



