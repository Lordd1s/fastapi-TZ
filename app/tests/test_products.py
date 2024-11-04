import pytest

from app.tests.conftest import async_db_session, async_client

TEST_DATA: dict = {
        'name': 'Test',
        'description': 'Some Description for test',
        'price': 1000,
        'quantity': 20
}


@pytest.mark.anyio
async def test_get_products(async_db_session, async_client):
    response = await async_client.get('/products/')
    assert response.status_code == 200


@pytest.mark.anyio
async def test_create_product(async_db_session, async_client):

    response = await async_client.post('/products/', json=TEST_DATA)
    response_data = response.json()
    assert response.status_code == 201
    assert response_data['name'] == 'Test'
    assert response_data['description'] == 'Some Description for test'
    assert response_data['price'] == 1000
    assert response_data['quantity'] == 20