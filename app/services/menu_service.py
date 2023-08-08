from fastapi import Depends
from redis import Redis

from ..caching import RedisCache, get_redis_client
from ..repositories.menu_repository import MenuRepository
from ..schemas import MenuCreate, MenuResponse, MenuUpdate


class MenuService:
    def __init__(self, menu_repository: MenuRepository = Depends(),
                 redis_client: Redis = Depends(get_redis_client)) -> None:
        self.menu_repository = menu_repository
        self.cache_client = RedisCache(redis_client)

    async def create_menu(self, menu_data: MenuCreate) -> MenuResponse:
        data = await self.menu_repository.create(menu_data)
        self.cache_client.set(f'/api/v1/menus/{data.id}', data)
        self.cache_client.set('/api/v1/menus', 'changed')
        return data

    async def read_menu(self, menu_id: str) -> MenuResponse:
        cached = self.cache_client.get(f'/api/v1/menus/{menu_id}')
        if cached and cached != 'changed':
            return cached
        data = await self.menu_repository.get_by_id(menu_id)
        self.cache_client.set(f'/api/v1/menus/{menu_id}', data)
        return data

    async def read_menus(self, skip: int = 0, limit: int = 100) -> list[MenuResponse]:
        cached = self.cache_client.get('/api/v1/menus')
        if cached and cached != 'changed':
            return cached
        data = await self.menu_repository.get_all(skip, limit)
        self.cache_client.set('/api/v1/menus', data)
        return data

    async def update_menu(self, menu_id: str, menu_data: MenuUpdate) -> MenuResponse:
        data = await self.menu_repository.update(menu_id, menu_data)
        self.cache_client.set(f'/api/v1/menus/{menu_id}', data)
        self.cache_client.set('/api/v1/menus', 'changed')
        return data

    async def delete_menu(self, menu_id: str) -> dict:
        self.cache_client.delete(f'/api/v1/menus/{menu_id}')
        self.cache_client.set('/api/v1/menus', 'changed')
        return await self.menu_repository.delete(menu_id)
