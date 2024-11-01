import enum
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text, String, func, Enum, ForeignKey

from app.database.db import Base

if TYPE_CHECKING:
    from app.models import Product


class OrderStatus(str, enum.Enum):
    IN_PROCESS = 'IN PROCESS'
    SHIPPED = 'SHIPPED'
    DELIVERED = 'DELIVED'


class Order(Base):
    date_created: Mapped[datetime] = mapped_column(default=func.now())
    status: Mapped[str] = mapped_column(default=OrderStatus.IN_PROCESS.value)
    order_items: Mapped[list['OrderItem']] = relationship(
        back_populates='order'
    )


class OrderItem(Base):
    order_id: Mapped[int] = mapped_column(
        ForeignKey('orders.id')
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey('products.id')
    )
    quantity: Mapped[int] = mapped_column(default=1)
    order: Mapped['Order'] = relationship(
        back_populates='order_items'
    )
    product: Mapped['Product'] = relationship(
        back_populates='order_items'
    )
