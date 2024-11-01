from fastapi import FastAPI
from app.api.product_api import router as product_router
from app.api.order_api import router as order_router

app = FastAPI()
app.include_router(product_router, tags=['products'])
app.include_router(order_router, tags=['orders'])

@app.get('/')
async def root():
    return {'message': 'hello'}

