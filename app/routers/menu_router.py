from fastapi import APIRouter, Depends

from ..schemas import MenuCreate, MenuResponse, MenuUpdate
from ..services.menu_service import MenuService

router = APIRouter()


@router.post('/menus', response_model=MenuResponse, status_code=201)
async def create_menu(menu_data: MenuCreate, response: MenuService = Depends()):
    return await response.create_menu(menu_data)


@router.get('/menus', response_model=list[MenuResponse])
async def read_menus(response: MenuService = Depends()):
    return await response.read_menus()


@router.get('/menus/{menu_id}', response_model=MenuResponse)
async def read_menu(menu_id: str, response: MenuService = Depends()):
    return await response.read_menu(menu_id)


@router.patch('/menus/{menu_id}', response_model=MenuResponse)
async def update_menu(menu_id: str, menu_data: MenuUpdate, response: MenuService = Depends()):
    return await response.update_menu(menu_id, menu_data)


@router.delete('/menus/{menu_id}')
async def delete_menu(menu_id: str, response: MenuService = Depends()):
    return await response.delete_menu(menu_id)
