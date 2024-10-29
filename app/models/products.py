from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text, String

from app.database.db import Base

class Product(Base):
    name: Mapped[str] = mapped_column(String(100), )
    description: Mapped[str] = mapped_column(
        Text,
        server_default='',
        default=''
    )
    price: Mapped[int] = mapped_column()
    quantity: Mapped[int] = mapped_column()
