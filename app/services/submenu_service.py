import redis
from fastapi import Depends

from ..caching import RedisCache, get_redis_client
from ..repositories.submenu_repository import SubMenuRepository
from ..schemas import SubMenuCreate, SubMenuUpdate


class SubMenuService:
    def __init__(self, submenu_repository: SubMenuRepository = Depends(),
                 redis_client: redis.Redis = Depends(get_redis_client)):
        self.submenu_repository = submenu_repository
        self.cache_client = RedisCache(redis_client)

    async def create_submenu(self, menu_id: str, submenu_data: SubMenuCreate):
        data = await self.submenu_repository.create(menu_id, submenu_data)
        self.cache_client.set(f'/api/v1/menus/{menu_id}/submenus/{data.id}', data)
        self.cache_client.set(f'/api/v1/menus/{menu_id}/submenus', 'changed')
        self.cache_client.set(f'/api/v1/menus/{menu_id}', 'changed')
        self.cache_client.set('/api/v1/menus', 'changed')
        return data

    async def read_submenu(self, menu_id: str, submenu_id: str):
        cached_menu = self.cache_client.get(f'/api/v1/menus/{menu_id}')
        if cached_menu:
            cached = self.cache_client.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
            if cached and cached != 'changed':
                return cached
        data = await self.submenu_repository.get_by_id(menu_id, submenu_id)
        self.cache_client.set(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}', data)
        return data

    async def read_submenus(self, menu_id: str, skip: int = 0, limit: int = 100):
        cached_menu = self.cache_client.get(f'/api/v1/menus/{menu_id}')
        if cached_menu:
            cached = self.cache_client.get(f'/api/v1/menus/{menu_id}/submenus')
            if cached and cached != 'changed':
                return cached
        data = await self.submenu_repository.get_all(menu_id, skip, limit)
        self.cache_client.set(f'/api/v1/menus/{menu_id}/submenus', data)
        return data

    async def update_submenu(self, menu_id: str, submenu_id: str, submenu_data: SubMenuUpdate):
        data = await self.submenu_repository.update(menu_id, submenu_id, submenu_data)
        self.cache_client.set(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}', data)
        self.cache_client.set(f'/api/v1/menus/{menu_id}/submenus', 'changed')
        return data

    async def delete_submenu(self, menu_id: str, submenu_id: str):
        self.cache_client.delete(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
        self.cache_client.set(f'/api/v1/menus/{menu_id}/submenus', 'changed')
        self.cache_client.set(f'/api/v1/menus/{menu_id}', 'changed')
        self.cache_client.set('/api/v1/menus', 'changed')
        return await self.submenu_repository.delete(menu_id, submenu_id)
