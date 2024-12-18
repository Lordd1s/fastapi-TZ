from typing import Annotated

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import db_manager
from app.models import Product

from app.crud import product_crud


async def product_by_id(
    product_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_manager.scoped_session_dependency),
) -> Product:
    product = await product_crud.get_product(session=session, product_id=product_id)
    if product is not None:
        return product

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Product id: {product_id} not found!",
    )


async def is_enough_product(
        product_id: Annotated[int, Path],
        quantity: int,
        session: AsyncSession
) -> bool:
    product_ = await product_by_id(product_id, session=session)
    return product_.quantity >= quantity


async def update_quantity(
        product_id: Annotated[int, Path],
        quantity: int,
        session: AsyncSession
) -> Product:
    product_ = await product_by_id(product_id, session=session)
    product_.quantity -= quantity

    session.add(product_)
    await session.commit()
    await session.refresh(product_)

    return product_
