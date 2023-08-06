import uuid

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..database import get_async_session
from ..models import Dish
from ..schemas import DishCreate, DishResponse, DishUpdate


class DishRepository:
    def __init__(self, db: AsyncSession = Depends(get_async_session)):
        self.db = db

    async def create(self, submenu_id, dish_data: DishCreate) -> DishResponse:
        Item: Dish = Dish(id=str(uuid.uuid4()), submenu_id=submenu_id, **dish_data.model_dump())
        self.db.add(Item)
        await self.db.commit()
        await self.db.refresh(Item)
        return DishResponse(**Item.__dict__)

    async def get_by_id(self, submenu_id: str, dish_id: str) -> DishResponse:
        stmt = select(Dish).filter(Dish.id == dish_id, Dish.submenu_id == submenu_id)
        result = await self.db.execute(stmt)
        Item: Dish = result.scalar()
        if not Item:
            raise HTTPException(status_code=404, detail='dish not found')
        return DishResponse(**Item.__dict__)

    async def get_all(self, submenu_id: str, skip: int = 0, limit: int = 100) -> list[DishResponse]:
        stmt = select(Dish).filter(Dish.submenu_id == submenu_id).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        dishes = result.scalars().all()
        dishes_list: list[DishResponse] = [DishResponse(**dish.__dict__) for dish in dishes]
        return dishes_list

    async def update(self, submenu_id: str, dish_id: str, dish_data: DishUpdate) -> DishResponse:
        stmt = select(Dish).filter(Dish.id == dish_id, Dish.submenu_id == submenu_id)
        result = await self.db.execute(stmt)
        Item: Dish = result.scalar()
        if not Item:
            raise HTTPException(status_code=404, detail='dish not found')

        for key, value in dish_data.dict(exclude_unset=True).items():
            setattr(Item, key, value)

        await self.db.commit()
        await self.db.refresh(Item)
        return DishResponse(**Item.__dict__)

    async def delete(self, submenu_id: str, dish_id: str):
        stmt = select(Dish).filter(Dish.id == dish_id, Dish.submenu_id == submenu_id)
        result = await self.db.execute(stmt)
        Item: Dish = result.scalar()

        if not Item:
            return {'status': False, 'message': 'dish not found'}

        await self.db.delete(Item)
        await self.db.commit()
        return {'status': True, 'message': 'The dish has been deleted'}
