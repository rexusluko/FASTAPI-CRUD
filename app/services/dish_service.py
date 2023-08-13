from fastapi import BackgroundTasks, Depends
from redis.asyncio import Redis

from ..caching import AsyncRedisCache, get_async_redis_client
from ..repositories.dish_repository import DishRepository
from ..schemas import DishCreate, DishResponse, DishUpdate


class DishService:
    def __init__(self, dish_repository: DishRepository = Depends(),
                 redis_client: Redis = Depends(get_async_redis_client)) -> None:
        self.dish_repository = dish_repository
        self.cache_client = AsyncRedisCache(redis_client)

    async def change_related_cache(self, menu_id: str, submenu_id: str) -> None:
        await self.cache_client.set(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', 'changed')
        await self.cache_client.set(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}', 'changed')
        await self.cache_client.set(f'/api/v1/menus/{menu_id}/submenus', 'changed')
        await self.cache_client.set(f'/api/v1/menus/{menu_id}', 'changed')
        await self.cache_client.set('/api/v1/menus', 'changed')
        await self.cache_client.delete('/api/v1/all')

    async def create_dish(self, menu_id: str, submenu_id: str, dish_data: DishCreate,
                          background_tasks: BackgroundTasks) -> DishResponse:
        data = await self.dish_repository.create(submenu_id, dish_data)
        background_tasks.add_task(self.cache_client.set,
                                  f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{data.id}', data)
        background_tasks.add_task(self.change_related_cache, menu_id, submenu_id)
        return data

    async def read_dish(self, menu_id, submenu_id: str, dish_id: str,
                        background_tasks: BackgroundTasks) -> DishResponse:
        cached_menu = await self.cache_client.get(f'/api/v1/menus/{menu_id}')
        if cached_menu:
            cached_submenu = await self.cache_client.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
            if cached_submenu:
                cached = await self.cache_client.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
                if cached:
                    return cached
        data = await self.dish_repository.get_by_id(submenu_id, dish_id)
        background_tasks.add_task(self.cache_client.set,
                                  f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', data)
        return data

    async def read_dishes(self, menu_id: str, submenu_id: str, background_tasks: BackgroundTasks, skip: int = 0,
                          limit: int = 100) -> list[DishResponse]:
        cached_menu = await self.cache_client.get(f'/api/v1/menus/{menu_id}')
        if cached_menu:
            cached_submenu = await self.cache_client.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
            if cached_submenu:
                cached = await self.cache_client.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes')
                if cached and cached != 'changed':
                    return cached
        data = await self.dish_repository.get_all(submenu_id, skip, limit)
        background_tasks.add_task(self.cache_client.set, f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', data)
        return data

    async def update_dish(self, menu_id: str, submenu_id: str, dish_id: str, dish_data: DishUpdate,
                          background_tasks: BackgroundTasks) -> DishResponse:
        data = await self.dish_repository.update(submenu_id, dish_id, dish_data)
        background_tasks.add_task(self.cache_client.set,
                                  f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', data)
        background_tasks.add_task(self.cache_client.set, f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
                                  'changed')
        background_tasks.add_task(self.cache_client.delete, '/api/v1/all')
        return data

    async def delete_dishes(self, menu_id: str, submenu_id: str, dish_id: str,
                            background_tasks: BackgroundTasks) -> dict:
        background_tasks.add_task(self.cache_client.delete,
                                  f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
        background_tasks.add_task(self.change_related_cache, menu_id, submenu_id)
        return await self.dish_repository.delete(submenu_id, dish_id)
