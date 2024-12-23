from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database.session import db_manager
from app.models import Order, Product
from app.crud import order_crud
from app.schemas import OrderRead, OrderCreate, OrderStatusUpdate
from app.services.order_services import order_by_id
from app.services.product_services import is_enough_product, update_quantity, product_by_id

router = APIRouter(prefix='/order')


@router.get('/', response_model=list[OrderRead], description='Все заказы')
async def get_orders(db: AsyncSession = Depends(db_manager.scoped_session_dependency)):
    return await order_crud.get_orders(session=db)


@router.get('/{order_id}', response_model=OrderRead, description='Заказ по id')
async def get_order(
        order: Order = Depends(order_by_id)
):
    return order


@router.post('/', response_model=OrderRead, description='Создание заказа', status_code=status.HTTP_201_CREATED)
async def create_order(order_in: OrderCreate, db: AsyncSession = Depends(db_manager.scoped_session_dependency)):
    order_dict = order_in.model_dump()
    is_enough = await is_enough_product(
        product_id=order_dict.get('product_id'),
        quantity=order_dict.get('quantity'),
        session=db
    )
    if is_enough:
        await update_quantity(
            product_id=order_dict.get('product_id'),
            quantity=order_dict.get('quantity'),
            session=db
        )
        return await order_crud.create_order(session=db, order_in=order_in)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Недостаточно количество товара')


@router.delete('/{order_id}',
               status_code=status.HTTP_204_NO_CONTENT,
               description='Удаление заказа')
async def delete_order(
        db: AsyncSession = Depends(db_manager.scoped_session_dependency),
        order: Order = Depends(order_by_id)
):
    print(order.id)
    return await order_crud.delete_order(
        session=db,
        order=order
    )


@router.patch(
    '/{order_id}',
    response_model=OrderRead,
    description='Обновление заказа'
)
async def update_order(
        order_update: OrderStatusUpdate,
        order: Order = Depends(order_by_id),
        db: AsyncSession = Depends(db_manager.scoped_session_dependency),
):
    return await order_crud.update_order(session=db, order=order, order_update=order_update)
