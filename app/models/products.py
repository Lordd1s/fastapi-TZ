from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text, String

from app.database.db import Base

if TYPE_CHECKING:
    from app.models import OrderItem

class Product(Base):
    name: Mapped[str] = mapped_column(String(100), )
    description: Mapped[str] = mapped_column(
        Text,
        server_default='',
        default=''
    )
    price: Mapped[int] = mapped_column()
    quantity: Mapped[int] = mapped_column()
    order_items: Mapped['OrderItem'] = relationship(
        back_populates='product'
    )