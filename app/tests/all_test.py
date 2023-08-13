import pytest
from httpx import AsyncClient

from ..main import app
from .conftest import URL


@pytest.mark.asyncio
async def test_get_all_entities():
    async with AsyncClient(app=app, base_url=URL) as client:
        create_menu_data = {'title': 'My menu 1', 'description': 'My menu description 1'}
        create_menu_response = await client.post('/api/v1/menus', json=create_menu_data)
        menu_id = create_menu_response.json()['id']
        create_submenu1_data = {'title': 'My submenu 1', 'description': 'My submenu description 1'}
        create_submenu1_response = await client.post(f'{URL}/api/v1/menus/{menu_id}/submenus',
                                                     json=create_submenu1_data)
        submenu1_id = create_submenu1_response.json()['id']
        create_submenu2_data = {'title': 'My submenu 2', 'description': 'My submenu description 2'}
        await client.post(f'{URL}/api/v1/menus/{menu_id}/submenus', json=create_submenu2_data)
        create_dish1_data = {'title': 'My dish 1', 'description': 'My dish description 1', 'price': '1'}
        await client.post(f'{URL}/api/v1/menus/{menu_id}/submenus/{submenu1_id}/dishes', json=create_dish1_data)
        create_dish2_data = {'title': 'My dish 2', 'description': 'My dish description 2', 'price': '2'}
        await client.post(f'{URL}/api/v1/menus/{menu_id}/submenus/{submenu1_id}/dishes', json=create_dish2_data)

        response = await client.get(f'{URL}/api/v1/all')

        assert response.status_code == 200

        result: list = response.json()

        assert len(result[0]['submenus']) == 2
        assert len(result[0]['submenus'][0]['dishes']) == 2
        assert len(result[0]['submenus'][1]['dishes']) == 0
