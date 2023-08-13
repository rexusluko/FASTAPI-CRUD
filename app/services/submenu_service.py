from fastapi import BackgroundTasks, Depends
from redis.asyncio import Redis

from ..caching import AsyncRedisCache, get_async_redis_client
from ..repositories.submenu_repository import SubMenuRepository
from ..schemas import SubMenuCreate, SubMenuResponse, SubMenuUpdate


class SubMenuService:
    def __init__(self, submenu_repository: SubMenuRepository = Depends(),
                 redis_client: Redis = Depends(get_async_redis_client)) -> None:
        self.submenu_repository = submenu_repository
        self.cache_client = AsyncRedisCache(redis_client)

    async def change_related_cache(self, menu_id: str) -> None:
        await self.cache_client.set(f'/api/v1/menus/{menu_id}/submenus', 'changed')
        await self.cache_client.set(f'/api/v1/menus/{menu_id}', 'changed')
        await self.cache_client.set('/api/v1/menus', 'changed')
        await self.cache_client.delete('/api/v1/all')

    async def create_submenu(self, menu_id: str, submenu_data: SubMenuCreate,
                             background_tasks: BackgroundTasks) -> SubMenuResponse:
        data = await self.submenu_repository.create(menu_id, submenu_data)
        background_tasks.add_task(self.cache_client.set, f'/api/v1/menus/{menu_id}/submenus/{data.id}', data)
        background_tasks.add_task(self.change_related_cache, menu_id)
        return data

    async def read_submenu(self, menu_id: str, submenu_id: str, background_tasks: BackgroundTasks) -> SubMenuResponse:
        cached_menu = await self.cache_client.get(f'/api/v1/menus/{menu_id}')
        if cached_menu:
            cached = await self.cache_client.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
            if cached and cached != 'changed':
                return cached
        data = await self.submenu_repository.get_by_id(menu_id, submenu_id)
        background_tasks.add_task(self.cache_client.set, f'/api/v1/menus/{menu_id}/submenus/{submenu_id}', data)
        return data

    async def read_submenus(self, menu_id: str, background_tasks: BackgroundTasks, skip: int = 0, limit: int = 100) -> list[SubMenuResponse]:
        cached_menu = await self.cache_client.get(f'/api/v1/menus/{menu_id}')
        if cached_menu:
            cached = await self.cache_client.get(f'/api/v1/menus/{menu_id}/submenus')
            if cached and cached != 'changed':
                return cached
        data = await self.submenu_repository.get_all(menu_id, skip, limit)
        background_tasks.add_task(self.cache_client.set, f'/api/v1/menus/{menu_id}/submenus', data)
        return data

    async def update_submenu(self, menu_id: str, submenu_id: str, submenu_data: SubMenuUpdate, background_tasks: BackgroundTasks) -> SubMenuResponse:
        data = await self.submenu_repository.update(menu_id, submenu_id, submenu_data)
        background_tasks.add_task(self.cache_client.set, f'/api/v1/menus/{menu_id}/submenus/{submenu_id}', data)
        background_tasks.add_task(self.cache_client.set, f'/api/v1/menus/{menu_id}/submenus', 'changed')
        background_tasks.add_task(self.cache_client.delete, '/api/v1/all')
        return data

    async def delete_submenu(self, menu_id: str, submenu_id: str, background_tasks: BackgroundTasks) -> dict:
        background_tasks.add_task(self.cache_client.delete, f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
        background_tasks.add_task(self.change_related_cache, menu_id)
        return await self.submenu_repository.delete(menu_id, submenu_id)
