from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import db_manager
from app.models import Product
from app.schemas import ProductRead, ProductCreate, ProductUpdate
from app.crud import product_crud
from app.services.product_services import product_by_id

router = APIRouter(prefix='/products')


@router.get('/', response_model=list[ProductRead], description='Список товаров')
async def get_products(db: AsyncSession = Depends(db_manager.scoped_session_dependency)):
    return await product_crud.get_products(db)


@router.get('/{product_id}', response_model=ProductRead, description='Получение информации о товаре по id')
async def get_product(product: Product = Depends(product_by_id)):
    return product


@router.post('/',
             response_model=ProductRead,
             status_code=status.HTTP_201_CREATED,
             description='Создание продукта'
             )
async def create_product(product_in: ProductCreate, db: AsyncSession = Depends(db_manager.scoped_session_dependency)):
    return await product_crud.create_product(session=db, product_in=product_in)


@router.put('/{product_id}',
            response_model=ProductRead,
            status_code=status.HTTP_200_OK,
            description='Обновление продукта')
async def update_product(
        product_update: ProductUpdate,
        product: Product = Depends(product_by_id),
        db: AsyncSession = Depends(db_manager.scoped_session_dependency)
):
    return await product_crud.update_product(
        session=db,
        product=product,
        product_update=product_update
    )


@router.delete('/{product_id}',
               status_code=status.HTTP_204_NO_CONTENT,
               description='Удаление продукта'
               )
async def delete_product(
        db: AsyncSession = Depends(db_manager.scoped_session_dependency),
        product: Product = Depends(product_by_id)
):
    return await product_crud.delete_product(
        session=db,
        product=product
    )
