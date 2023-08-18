import pytest
from httpx import AsyncClient

from app.tests.conftest import URL


@pytest.mark.asyncio
async def test_create_dish(async_client: AsyncClient):
    async for client in async_client:
        create_menu_data = {'title': 'My menu 11', 'description': 'My menu description 11'}
        create_menu_response = await client.post('/api/v1/menus', json=create_menu_data)
        menu_id = create_menu_response.json()['id']
        create_submenu_data = {'title': 'My submenu 11', 'description': 'My menu description 11'}
        create_submenu_response = await client.post(f'{URL}/api/v1/menus/{menu_id}/submenus', json=create_submenu_data)
        submenu_id = create_submenu_response.json()['id']
        data = {'title': 'My dish 111', 'description': 'My dish description 111', 'price': '100'}
        response = await client.post(f'{URL}/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', json=data)

        assert response.status_code == 201
        assert 'id' in response.json()
        assert response.json()['title'] == data['title']
        assert response.json()['description'] == data['description']
        assert response.json()['price'] == data['price']


@pytest.mark.asyncio
async def test_get_dishes(async_client: AsyncClient):
    async for client in async_client:
        create_menu_data = {'title': 'My menu 11', 'description': 'My menu description 11'}
        create_menu_response = await client.post('/api/v1/menus', json=create_menu_data)
        menu_id = create_menu_response.json()['id']
        create_submenu_data = {'title': 'My submenu 11', 'description': 'My menu description 11'}
        create_submenu_response = await client.post(f'{URL}/api/v1/menus/{menu_id}/submenus', json=create_submenu_data)
        submenu_id = create_submenu_response.json()['id']
        response = await client.get(f'{URL}/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes')
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_dish(async_client: AsyncClient):
    async for client in async_client:
        create_menu_data = {'title': 'My menu 11', 'description': 'My menu description 11'}
        create_menu_response = await client.post('/api/v1/menus', json=create_menu_data)
        menu_id = create_menu_response.json()['id']
        create_submenu_data = {'title': 'My submenu 11', 'description': 'My menu description 11'}
        create_submenu_response = await client.post(f'{URL}/api/v1/menus/{menu_id}/submenus', json=create_submenu_data)
        submenu_id = create_submenu_response.json()['id']
        create_dish_data = {'title': 'My dish 111', 'description': 'My dish description 111', 'price': '100'}
        create_dish_response = await client.post(f'{URL}/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', json=create_dish_data)
        dish_id = create_dish_response.json()['id']

        response = await client.get(f'{URL}/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
        assert response.status_code == 200
        assert 'id' in response.json()
        assert 'title' in response.json()
        assert 'description' in response.json()
        assert 'price' in response.json()


@pytest.mark.asyncio
async def test_get_non_existing_dish(async_client: AsyncClient):
    async for client in async_client:
        create_menu_data = {'title': 'My menu 11', 'description': 'My menu description 11'}
        create_menu_response = await client.post('/api/v1/menus', json=create_menu_data)
        menu_id = create_menu_response.json()['id']
        create_submenu_data = {'title': 'My submenu 11', 'description': 'My menu description 11'}
        create_submenu_response = await client.post(f'{URL}/api/v1/menus/{menu_id}/submenus', json=create_submenu_data)
        submenu_id = create_submenu_response.json()['id']

        response = await client.get(f'{URL}/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/None')

        assert response.status_code == 404
        assert response.json()['detail'] == 'dish not found'


@pytest.mark.asyncio
async def test_update_dish(async_client: AsyncClient):
    async for client in async_client:
        create_menu_data = {'title': 'My menu 11', 'description': 'My menu description 11'}
        create_menu_response = await client.post('/api/v1/menus', json=create_menu_data)
        menu_id = create_menu_response.json()['id']
        create_submenu_data = {'title': 'My submenu 11', 'description': 'My menu description 11'}
        create_submenu_response = await client.post(f'{URL}/api/v1/menus/{menu_id}/submenus', json=create_submenu_data)
        submenu_id = create_submenu_response.json()['id']
        create_dish_data = {'title': 'My dish 111', 'description': 'My dish description 111', 'price': '100'}
        create_dish_response = await client.post(f'{URL}/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', json=create_dish_data)
        dish_id = create_dish_response.json()['id']

        data = {'title': 'My dish 22111', 'description': 'My dish description 1112', 'price': '1300'}

        response = await client.patch(f'{URL}/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', json=data)

        assert response.json()['id'] == dish_id
        assert response.json()['title'] == data['title']
        assert response.json()['description'] == data['description']
        assert response.json()['price'] == data['price']


@pytest.mark.asyncio
async def test_update_non_existing_dish(async_client: AsyncClient):
    async for client in async_client:
        create_menu_data = {'title': 'My menu 11', 'description': 'My menu description 11'}
        create_menu_response = await client.post('/api/v1/menus', json=create_menu_data)
        menu_id = create_menu_response.json()['id']
        create_submenu_data = {'title': 'My submenu 11', 'description': 'My menu description 11'}
        create_submenu_response = await client.post(f'{URL}/api/v1/menus/{menu_id}/submenus', json=create_submenu_data)
        submenu_id = create_submenu_response.json()['id']

        data = {'title': 'My dish 22111', 'description': 'My dish description 1112', 'price': '1300'}

        response = await client.patch(f'{URL}/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/None', json=data)
        assert response.status_code == 404
        assert response.json()['detail'] == 'dish not found'


@pytest.mark.asyncio
async def test_delete_submenu(async_client: AsyncClient):
    async for client in async_client:
        create_menu_data = {'title': 'My menu 11', 'description': 'My menu description 11'}
        create_menu_response = await client.post('/api/v1/menus', json=create_menu_data)
        menu_id = create_menu_response.json()['id']
        create_submenu_data = {'title': 'My submenu 11', 'description': 'My menu description 11'}
        create_submenu_response = await client.post(f'{URL}/api/v1/menus/{menu_id}/submenus', json=create_submenu_data)
        submenu_id = create_submenu_response.json()['id']
        create_dish_data = {'title': 'My dish 111', 'description': 'My dish description 111', 'price': '100'}
        create_dish_response = await client.post(f'{URL}/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', json=create_dish_data)
        dish_id = create_dish_response.json()['id']

        response = await client.delete(f'{URL}/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
        assert response.status_code == 200
        assert response.json()['status'] is True
        assert response.json()['message'] == 'The dish has been deleted'
