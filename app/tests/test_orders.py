from itertools import product

import pytest

from app.tests.conftest import async_db_session, async_client
from app.tests.test_products import TEST_DATA as TEST_PRODUCT_DATA

TEST_DATA: dict = {
    "status": "IN_PROCESS",
    "product_id": 1,
    "quantity": 1
}


@pytest.mark.anyio
async def test_get_orders(async_db_session, async_client):
    response = await async_client.get('/order/')
    assert response.status_code == 200


@pytest.mark.anyio
async def test_create_order(async_db_session, async_client):
    product_response = await async_client.post('/products/', json=TEST_PRODUCT_DATA)

    TEST_DATA['product_id'] = product_response.json()['id']
    response = await async_client.post('/order/', json=TEST_DATA)

    assert response.status_code == 201
    response_data = response.json()
    assert response_data['status'] == 'IN_PROCESS'
