from typing import List
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models import OrderStatus


class OrderBase(BaseModel):
    status: OrderStatus = OrderStatus.IN_PROCESS


class OrderCreate(OrderBase):
    pass


class OrderUpdate(OrderCreate):
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
