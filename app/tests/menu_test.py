import pytest
from httpx import AsyncClient

from ..main import app
from .conftest import URL


@pytest.mark.asyncio
async def test_create_menu():
    async with AsyncClient(app=app, base_url=URL) as client:
        data = {'title': 'My menu 1', 'description': 'My menu description 1'}
        response = await client.post(f'{URL}/api/v1/menus', json=data)

        assert response.status_code == 201
        assert 'id' in response.json()
        assert response.json()['title'] == data['title']
        assert response.json()['description'] == data['description']
        assert 'submenus_count' in response.json()
        assert 'dishes_count' in response.json()


@pytest.mark.asyncio
async def test_get_menus():
    async with AsyncClient(app=app, base_url=URL) as client:
        response = await client.get(f'{URL}/api/v1/menus')
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_menu():
    async with AsyncClient(app=app, base_url=URL) as client:
        create_data = {'title': 'My menu 2', 'description': 'My menu description 2'}
        create_response = await client.post('/api/v1/menus', json=create_data)
        menu_id = create_response.json()['id']

        response = await client.get(f'{URL}/api/v1/menus/{menu_id}')
        assert response.status_code == 200
        assert 'id' in response.json()
        assert 'title' in response.json()
        assert 'description' in response.json()
        assert 'submenus_count' in response.json()


@pytest.mark.asyncio
async def test_get_non_existing_menu():
    async with AsyncClient(app=app, base_url=URL) as client:
        response = await client.get(f'{URL}/api/v1/menus/None')

        assert response.status_code == 404
        assert response.json()['detail'] == 'menu not found'


@pytest.mark.asyncio
async def test_update_menu():
    async with AsyncClient(app=app, base_url=URL) as client:
        create_data = {'title': 'My menu 3', 'description': 'My menu description 3'}
        create_response = await client.post('/api/v1/menus', json=create_data)
        menu_id = create_response.json()['id']

        data = {'title': 'Changed menu 1', 'description': 'Changed description 1'}
        response = await client.patch(f'{URL}/api/v1/menus/{menu_id}', json=data)
        assert response.status_code == 200
        assert response.json()['id'] == menu_id
        assert response.json()['title'] == data['title']
        assert response.json()['description'] == data['description']
        assert 'submenus_count' in response.json()
        assert 'dishes_count' in response.json()


@pytest.mark.asyncio
async def test_update_non_existing_menu():
    async with AsyncClient(app=app, base_url=URL) as client:
        data = {'title': 'Changed menu 1', 'description': 'Changed description 1'}
        response = await client.patch(f'{URL}/api/v1/menus/None', json=data)
        assert response.status_code == 404
        assert response.json()['detail'] == 'menu not found'


@pytest.mark.asyncio
async def test_delete_menu():
    async with AsyncClient(app=app, base_url=URL) as client:
        create_data = {'title': 'My menu 4', 'description': 'My menu description 4'}
        create_response = await client.post('/api/v1/menus', json=create_data)
        menu_id = create_response.json()['id']

        response = await client.delete(f'{URL}/api/v1/menus/{menu_id}')
        assert response.status_code == 200
        assert response.json()['status'] is True
        assert response.json()['message'] == 'The menu has been deleted'
