from fastapi import APIRouter, BackgroundTasks, Depends

from ..schemas import MenuCreate, MenuResponse, MenuUpdate
from ..services.menu_service import MenuService

router = APIRouter()


@router.post('/menus', response_model=MenuResponse, status_code=201)
async def create_menu(menu_data: MenuCreate, background_tasks: BackgroundTasks,
                      response: MenuService = Depends()) -> MenuResponse:
    return await response.create_menu(menu_data, background_tasks)


@router.get('/menus', response_model=list[MenuResponse])
async def read_menus(background_tasks: BackgroundTasks, response: MenuService = Depends()) -> list[MenuResponse]:
    return await response.read_menus(background_tasks)


@router.get('/menus/{menu_id}', response_model=MenuResponse)
async def read_menu(menu_id: str, background_tasks: BackgroundTasks, response: MenuService = Depends()) -> MenuResponse:
    return await response.read_menu(menu_id, background_tasks)


@router.patch('/menus/{menu_id}', response_model=MenuResponse)
async def update_menu(menu_id: str, background_tasks: BackgroundTasks, menu_data: MenuUpdate,
                      response: MenuService = Depends()) -> MenuResponse:
    return await response.update_menu(menu_id, menu_data, background_tasks)


@router.delete('/menus/{menu_id}')
async def delete_menu(menu_id: str, background_tasks: BackgroundTasks, response: MenuService = Depends()) -> dict:
    return await response.delete_menu(menu_id, background_tasks)


@router.get('/all')
async def read_all(background_tasks: BackgroundTasks, response: MenuService = Depends()) -> list[dict]:
    return await response.read_all(background_tasks)
