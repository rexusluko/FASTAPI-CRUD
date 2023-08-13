from fastapi import BackgroundTasks, Depends
from redis.asyncio import Redis

from ..caching import AsyncRedisCache, get_async_redis_client
from ..repositories.menu_repository import MenuRepository
from ..schemas import MenuCreate, MenuResponse, MenuUpdate


class MenuService:
    def __init__(self, menu_repository: MenuRepository = Depends(),
                 redis_client: Redis = Depends(get_async_redis_client)) -> None:
        self.menu_repository = menu_repository
        self.cache_client = AsyncRedisCache(redis_client)

    async def change_related_cache(self) -> None:
        await self.cache_client.set('/api/v1/menus', 'changed')
        await self.cache_client.delete('/api/v1/all')

    async def create_menu(self, menu_data: MenuCreate, background_tasks: BackgroundTasks) -> MenuResponse:
        data = await self.menu_repository.create(menu_data)
        background_tasks.add_task(self.cache_client.set, f'/api/v1/menus/{data.id}', data)
        background_tasks.add_task(self.change_related_cache)
        return data

    async def read_menu(self, menu_id: str, background_tasks: BackgroundTasks) -> MenuResponse:
        cached = await self.cache_client.get(f'/api/v1/menus/{menu_id}')
        if cached and cached != 'changed':
            return cached
        data = await self.menu_repository.get_by_id(menu_id)
        background_tasks.add_task(self.cache_client.set, f'/api/v1/menus/{menu_id}', data)
        return data

    async def read_menus(self, background_tasks: BackgroundTasks, skip: int = 0, limit: int = 100) -> list[
            MenuResponse]:
        cached = await self.cache_client.get('/api/v1/menus')
        if cached and cached != 'changed':
            return cached
        data = await self.menu_repository.get_all(skip, limit)
        background_tasks.add_task(self.cache_client.set, '/api/v1/menus', data)
        return data

    async def update_menu(self, menu_id: str, menu_data: MenuUpdate, background_tasks: BackgroundTasks) -> MenuResponse:
        data = await self.menu_repository.update(menu_id, menu_data)
        background_tasks.add_task(self.cache_client.set, f'/api/v1/menus/{menu_id}', data)
        background_tasks.add_task(self.change_related_cache)
        return data

    async def delete_menu(self, menu_id: str, background_tasks: BackgroundTasks) -> dict:
        background_tasks.add_task(self.cache_client.delete, f'/api/v1/menus/{menu_id}')
        background_tasks.add_task(self.change_related_cache)
        return await self.menu_repository.delete(menu_id)

    async def read_all(self, background_tasks: BackgroundTasks) -> list[dict]:
        cached = await self.cache_client.get('/api/v1/all')
        if cached:
            return cached
        data = await self.menu_repository.get_all_entities()
        background_tasks.add_task(self.cache_client.set, '/api/v1/all', data)
        return data
