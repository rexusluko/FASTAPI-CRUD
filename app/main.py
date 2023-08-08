import redis  # type: ignore
from fastapi import FastAPI

from app.routers import dish_router, menu_router, submenu_router

from .database import create_tables

app: FastAPI = FastAPI()

app.include_router(menu_router.router, prefix='/api/v1', tags=['menus'])
app.include_router(submenu_router.router, prefix='/api/v1/menus/{menu_id}', tags=['submenus'])
app.include_router(dish_router.router, prefix='/api/v1/menus/{menu_id}/submenus/{submenu_id}', tags=['dishes'])

redis_client: redis.Redis = redis.Redis(host='localhost', port=6379)


async def startup_event() -> None:
    await create_tables()


app.add_event_handler('startup', startup_event)
