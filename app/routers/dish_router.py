from fastapi import APIRouter, BackgroundTasks, Depends

from ..schemas import DishCreate, DishResponse, DishUpdate
from ..services.dish_service import DishService

router = APIRouter()


@router.post('/dishes', response_model=DishResponse, status_code=201)
async def create_dish(menu_id: str, submenu_id: str, dish_data: DishCreate, background_tasks: BackgroundTasks, response: DishService = Depends()) -> DishResponse:
    return await response.create_dish(menu_id, submenu_id, dish_data, background_tasks)


@router.get('/dishes', response_model=list[DishResponse])
async def read_dishes(menu_id: str, submenu_id: str, background_tasks: BackgroundTasks, response: DishService = Depends()) -> list[DishResponse]:
    return await response.read_dishes(menu_id, submenu_id, background_tasks)


@router.get('/dishes/{dish_id}', response_model=DishResponse)
async def read_dish(menu_id: str, submenu_id: str, dish_id: str, background_tasks: BackgroundTasks, response: DishService = Depends()) -> DishResponse:
    return await response.read_dish(menu_id, submenu_id, dish_id, background_tasks)


@router.patch('/dishes/{dish_id}', response_model=DishResponse)
async def update_dish(menu_id: str, submenu_id: str, dish_id: str, dish_data: DishUpdate, background_tasks: BackgroundTasks,
                      response: DishService = Depends()) -> DishResponse:
    return await response.update_dish(menu_id, submenu_id, dish_id, dish_data, background_tasks)


@router.delete('/dishes/{dish_id}')
async def delete_dish(menu_id: str, submenu_id: str, dish_id: str, background_tasks: BackgroundTasks, response: DishService = Depends()) -> dict:
    return await response.delete_dishes(menu_id, submenu_id, dish_id, background_tasks)
