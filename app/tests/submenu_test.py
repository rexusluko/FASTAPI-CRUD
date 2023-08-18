import pytest
from httpx import AsyncClient

from app.tests.conftest import URL


@pytest.mark.asyncio
async def test_create_submenu(async_client: AsyncClient):
    async for client in async_client:
        create_menu_data = {'title': 'My menu 11', 'description': 'My menu description 11'}
        create_menu_response = await client.post('/api/v1/menus', json=create_menu_data)
        menu_id = create_menu_response.json()['id']
        data = {'title': 'My submenu 11', 'description': 'My menu description 11'}
        response = await client.post(f'{URL}/api/v1/menus/{menu_id}/submenus', json=data)

        assert response.status_code == 201
        assert 'id' in response.json()
        assert response.json()['title'] == data['title']
        assert response.json()['description'] == data['description']
        assert 'dishes_count' in response.json()
        return response.json()


@pytest.mark.asyncio
async def test_get_submenus(async_client: AsyncClient):
    async for client in async_client:
        create_menu_data = {'title': 'My menu 12', 'description': 'My menu description 12'}
        create_menu_response = await client.post('/api/v1/menus', json=create_menu_data)
        menu_id = create_menu_response.json()['id']
        response = await client.get(f'{URL}/api/v1/menus/{menu_id}/submenus')
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_submenu(async_client: AsyncClient):
    async for client in async_client:
        create_menu_data = {'title': 'My menu 13', 'description': 'My menu description 13'}
        create_menu_response = await client.post('/api/v1/menus', json=create_menu_data)
        menu_id = create_menu_response.json()['id']

        create_data = {'title': 'My submenu 13', 'description': 'My menu description 13'}
        create_response = await client.post(f'{URL}/api/v1/menus/{menu_id}/submenus', json=create_data)
        submenu_id = create_response.json()['id']

        response = await client.get(f'{URL}/api/v1/menus/{menu_id}/submenus/{submenu_id}')
        assert response.status_code == 200
        assert 'id' in response.json()
        assert 'title' in response.json()
        assert 'description' in response.json()
        assert 'dishes_count' in response.json()


@pytest.mark.asyncio
async def test_get_non_existing_submenu(async_client: AsyncClient):
    async for client in async_client:
        create_menu_data = {'title': 'My menu 14', 'description': 'My menu description 14'}
        create_menu_response = await client.post('/api/v1/menus', json=create_menu_data)
        menu_id = create_menu_response.json()['id']

        response = await client.get(f'{URL}/api/v1/menus/{menu_id}/submenus/None')

        assert response.status_code == 404
        assert response.json()['detail'] == 'submenu not found'


@pytest.mark.asyncio
async def test_update_submenu(async_client: AsyncClient):
    async for client in async_client:
        create_menu_data = {'title': 'My menu 14', 'description': 'My menu description 14'}
        create_menu_response = await client.post('/api/v1/menus', json=create_menu_data)
        menu_id = create_menu_response.json()['id']

        create_data = {'title': 'My submenu 14', 'description': 'My menu description 14'}
        create_response = await client.post(f'{URL}/api/v1/menus/{menu_id}/submenus', json=create_data)
        submenu_id = create_response.json()['id']

        data = {'title': 'Changed submenu 14', 'description': 'Changed description 14'}
        response = await client.patch(f'{URL}/api/v1/menus/{menu_id}/submenus/{submenu_id}', json=data)
        assert response.status_code == 200
        assert response.json()['id'] == submenu_id
        assert response.json()['title'] == data['title']
        assert response.json()['description'] == data['description']
        assert 'dishes_count' in response.json()


@pytest.mark.asyncio
async def test_update_non_existing_submenu(async_client: AsyncClient):
    async for client in async_client:
        create_menu_data = {'title': 'My menu 14', 'description': 'My menu description 14'}
        create_menu_response = await client.post('/api/v1/menus', json=create_menu_data)
        menu_id = create_menu_response.json()['id']

        data = {'title': 'Changed menu 16', 'description': 'Changed description 16'}
        response = await client.patch(f'{URL}/api/v1/menus/{menu_id}/submenus/None', json=data)
        assert response.status_code == 404
        assert response.json()['detail'] == 'submenu not found'


@pytest.mark.asyncio
async def test_delete_submenu(async_client: AsyncClient):
    async for client in async_client:
        create_menu_data = {'title': 'My menu 17', 'description': 'My menu description 17'}
        create_menu_response = await client.post('/api/v1/menus', json=create_menu_data)
        menu_id = create_menu_response.json()['id']

        create_data = {'title': 'My submenu 17', 'description': 'My menu description 17'}
        create_response = await client.post(f'{URL}/api/v1/menus/{menu_id}/submenus', json=create_data)
        submenu_id = create_response.json()['id']

        response = await client.delete(f'{URL}/api/v1/menus/{menu_id}/submenus/{submenu_id}')
        assert response.status_code == 200
        assert response.json()['status'] is True
        assert response.json()['message'] == 'The submenu has been deleted'
