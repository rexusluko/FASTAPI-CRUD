import uuid

from fastapi import Depends, HTTPException
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..database import get_async_session
from ..models import Menu
from ..schemas import MenuCreate, MenuResponse, MenuUpdate


class MenuRepository:
    def __init__(self, db: AsyncSession = Depends(get_async_session)):
        self.db = db

    async def create(self, menu_data: MenuCreate) -> MenuResponse:
        Item: Menu = Menu(id=str(uuid.uuid4()), **menu_data.model_dump())
        self.db.add(Item)
        await self.db.commit()
        await self.db.refresh(Item)
        return MenuResponse(**Item.__dict__)

    async def get_by_id(self, menu_id: str) -> MenuResponse:
        stmt = select(Menu).filter(Menu.id == menu_id)
        result = await self.db.execute(stmt)
        Item: Menu = result.scalar()
        if not Item:
            raise HTTPException(status_code=404, detail='menu not found')
        return MenuResponse(**Item.__dict__)

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[MenuResponse]:
        stmt = select(Menu).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        menus = result.scalars().all()
        menus_list: list[MenuResponse] = [MenuResponse(**menu.__dict__) for menu in menus]
        return menus_list

    async def update(self, menu_id: str, menu_data: MenuUpdate) -> MenuResponse:
        stmt = select(Menu).filter(Menu.id == menu_id)
        result = await self.db.execute(stmt)
        Item: Menu = result.scalar()
        if not Item:
            raise HTTPException(status_code=404, detail='menu not found')

        for key, value in menu_data.dict(exclude_unset=True).items():
            setattr(Item, key, value)

        await self.db.commit()
        await self.db.refresh(Item)
        return MenuResponse(**Item.__dict__)

    async def delete(self, menu_id: str):
        stmt = select(Menu).filter(Menu.id == menu_id)
        result = await self.db.execute(stmt)
        Item: Menu = result.scalar()

        if not Item:
            return {'status': False, 'message': 'menu not found'}

        await self.db.execute(delete(Menu).where(Menu.id == menu_id))
        await self.db.commit()
        return {'status': True, 'message': 'The menu has been deleted'}
