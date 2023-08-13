import pytest
from httpx import AsyncClient

from ..main import app
from .conftest import URL


@pytest.mark.asyncio
async def test_count():
    async with AsyncClient(app=app, base_url=URL) as client:
        create_menu_data = {'title': 'My menu 1', 'description': 'My menu description 1'}
        create_menu_response = await client.post('/api/v1/menus', json=create_menu_data)
        menu_id = create_menu_response.json()['id']
        create_submenu_data = {'title': 'My submenu 1', 'description': 'My submenu description 1'}
        create_submenu_response = await client.post(f'{URL}/api/v1/menus/{menu_id}/submenus', json=create_submenu_data)
        submenu_id = create_submenu_response.json()['id']
        create_dish1_data = {'title': 'My dish 1', 'description': 'My dish description 1', 'price': '1'}
        await client.post(f'{URL}/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', json=create_dish1_data)
        create_dish2_data = {'title': 'My dish 2', 'description': 'My dish description 2', 'price': '2'}
        await client.post(f'{URL}/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', json=create_dish2_data)
        menu_response = await client.get(f'{URL}/api/v1/menus/{menu_id}')
        menu_data = menu_response.json()
        assert menu_data['submenus_count'] == 1
        assert menu_data['dishes_count'] == 2
        submenu_response = await client.get(f'{URL}/api/v1/menus/{menu_id}/submenus/{submenu_id}')
        submenu_data = submenu_response.json()
        assert submenu_data['dishes_count'] == 2
        await client.delete(f'{URL}/api/v1/menus/{menu_id}/submenus/{submenu_id}')
        menu_submenus_response = await client.get(f'{URL}/api/v1/menus/{menu_id}/submenus')
        assert menu_submenus_response.json() == []
        submenu_dishes_response = await client.get(f'{URL}/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes')
        assert submenu_dishes_response.json() == []
        menu_response = await client.get(f'{URL}/api/v1/menus/{menu_id}')
        menu_data = menu_response.json()
        assert menu_data['submenus_count'] == 0
        assert menu_data['dishes_count'] == 0
        await client.delete(f'{URL}/api/v1/menus/{menu_id}')
