from typing import List
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models import OrderStatus


class OrderBase(BaseModel):
    status: OrderStatus


class OrderCreate(OrderBase):
    product_id: int
    quantity: int = 1

class OrderStatusUpdate(OrderBase):
    pass


class OrderRead(OrderBase):
    id: int
    date_created: datetime
    order_items: List['OrderItemRead'] = []


class OrderItemBase(BaseModel):
    order_id: int
    product_id: int
    quantity: int = 1


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemRead(OrderItemBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
