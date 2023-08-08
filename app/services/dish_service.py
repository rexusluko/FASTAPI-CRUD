import redis
from fastapi import Depends

from ..caching import RedisCache, get_redis_client
from ..repositories.dish_repository import DishRepository
from ..schemas import DishCreate, DishResponse, DishUpdate


class DishService:
    def __init__(self, dish_repository: DishRepository = Depends(),
                 redis_client: redis.Redis = Depends(get_redis_client)) -> None:
        self.dish_repository = dish_repository
        self.cache_client = RedisCache(redis_client)

    def change_related_cache(self, menu_id: str, submenu_id: str) -> None:
        self.cache_client.set(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', 'changed')
        self.cache_client.set(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}', 'changed')
        self.cache_client.set(f'/api/v1/menus/{menu_id}/submenus', 'changed')
        self.cache_client.set(f'/api/v1/menus/{menu_id}', 'changed')
        self.cache_client.set('/api/v1/menus', 'changed')

    async def create_dish(self, menu_id: str, submenu_id: str, dish_data: DishCreate) -> DishResponse:
        data = await self.dish_repository.create(submenu_id, dish_data)
        self.cache_client.set(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{data.id}', data)
        self.change_related_cache(menu_id, submenu_id)
        return data

    async def read_dish(self, menu_id, submenu_id: str, dish_id: str) -> DishResponse:
        cached_menu = self.cache_client.get(f'/api/v1/menus/{menu_id}')
        if cached_menu:
            cached_submenu = self.cache_client.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
            if cached_submenu:
                cached = self.cache_client.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
                if cached:
                    return cached
        data = await self.dish_repository.get_by_id(submenu_id, dish_id)
        self.cache_client.set(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', data)
        return data

    async def read_dishes(self, menu_id: str, submenu_id: str, skip: int = 0, limit: int = 100) -> list[DishResponse]:
        cached_menu = self.cache_client.get(f'/api/v1/menus/{menu_id}')
        if cached_menu:
            cached_submenu = self.cache_client.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
            if cached_submenu:
                cached = self.cache_client.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes')
                if cached and cached != 'changed':
                    return cached
        data = await self.dish_repository.get_all(submenu_id, skip, limit)
        self.cache_client.set(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', data)
        return data

    async def update_dish(self, menu_id: str, submenu_id: str, dish_id: str, dish_data: DishUpdate) -> DishResponse:
        data = await self.dish_repository.update(submenu_id, dish_id, dish_data)
        self.cache_client.set(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', data)
        self.cache_client.set(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', 'changed')
        return data

    async def delete_dishes(self, menu_id: str, submenu_id: str, dish_id: str) -> dict:
        self.cache_client.delete(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
        self.change_related_cache(menu_id, submenu_id)
        return await self.dish_repository.delete(submenu_id, dish_id)
