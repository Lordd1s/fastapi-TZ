from typing import Annotated

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import db_manager
from app.models import Order

from app.crud import order_crud


async def order_by_id(
    order_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_manager.scoped_session_dependency),
) -> Order:
    order = await order_crud.get_order(session=session, order_id=order_id)
    if order is not None:
        return order

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Order id: {order_id} not found!"
    )