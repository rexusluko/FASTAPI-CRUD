from fastapi import APIRouter, Depends

from ..schemas import SubMenuCreate, SubMenuResponse, SubMenuUpdate
from ..services.submenu_service import SubMenuService

router = APIRouter()


@router.post('/submenus', response_model=SubMenuResponse, status_code=201)
async def create_submenu(menu_id: str, submenu_data: SubMenuCreate, response: SubMenuService = Depends()):
    return await response.create_submenu(menu_id, submenu_data)


@router.get('/submenus', response_model=list[SubMenuResponse])
async def read_submenus(menu_id: str, response: SubMenuService = Depends()):
    return await response.read_submenus(menu_id)


@router.get('/submenus/{submenu_id}', response_model=SubMenuResponse)
async def read_submenu(menu_id: str, submenu_id: str, response: SubMenuService = Depends()):
    return await response.read_submenu(menu_id, submenu_id)


@router.patch('/submenus/{submenu_id}', response_model=SubMenuResponse)
async def update_submenu(menu_id: str, submenu_id: str, submenu_data: SubMenuUpdate,
                         response: SubMenuService = Depends()):
    return await response.update_submenu(menu_id, submenu_id, submenu_data)


@router.delete('/submenus/{submenu_id}')
async def delete_submenu(menu_id: str, submenu_id: str, response: SubMenuService = Depends()):
    return await response.delete_submenu(menu_id, submenu_id)
