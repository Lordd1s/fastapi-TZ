
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Order, OrderItem
from app.schemas import OrderCreate, OrderStatusUpdate
from app.services.product_services import product_by_id
from app.services.order_services import order_by_id


async def get_orders(session: AsyncSession) -> list[Order]:
    stmt = select(Order).options(
        selectinload(Order.order_items).joinedload(OrderItem.product)
    ).order_by(Order.id)
    result: Result = await session.execute(stmt)
    orders = result.scalars().all()
    return list(orders)


async def get_order(session: AsyncSession, order_id: int) -> Order | None:
    stmt = select(Order).options(
        selectinload(Order.order_items).joinedload(OrderItem.product)
    ).filter(Order.id == order_id)
    order: Order | None = await session.scalar(stmt)
    return order


async def create_order(session: AsyncSession, order_in: OrderCreate) -> Order:
    order_dict = order_in.model_dump()
    new_order = Order(status=order_dict['status'])
    product = await product_by_id(
        product_id=order_dict.get('product_id'),
        session=session
    )

    order_item = OrderItem(
            product_id=product.id,
            quantity=order_dict['quantity']
        )
    new_order.order_items.append(order_item)

    session.add(new_order)
    await session.commit()

    loaded_order = await order_by_id(
        order_id=new_order.id,
        session=session
    )
    return loaded_order


async def update_order(
    session: AsyncSession,
    order: Order,
    order_update: OrderStatusUpdate,
) -> Order:
    for name, value in order_update.model_dump().items():
        setattr(order, name, value)
    await session.commit()
    return order


async def delete_order(
    session: AsyncSession,
    order: Order,
) -> None:
    await session.delete(order)
    await session.commit()
