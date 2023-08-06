import uuid

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..database import get_async_session
from ..models import SubMenu
from ..schemas import SubMenuCreate, SubMenuResponse, SubMenuUpdate


class SubMenuRepository:
    def __init__(self, db: AsyncSession = Depends(get_async_session)):
        self.db = db

    async def create(self, menu_id, submenu_data: SubMenuCreate) -> SubMenuResponse:
        Item: SubMenu = SubMenu(id=str(uuid.uuid4()), menu_id=menu_id, **submenu_data.model_dump())
        self.db.add(Item)
        await self.db.commit()
        await self.db.refresh(Item)
        return SubMenuResponse(**Item.__dict__)

    async def get_by_id(self, menu_id: str, submenu_id: str) -> SubMenuResponse:
        stmt = select(SubMenu).filter(SubMenu.id == submenu_id, SubMenu.menu_id == menu_id)
        result = await self.db.execute(stmt)
        Item: SubMenu = result.scalar()
        if not Item:
            raise HTTPException(status_code=404, detail='submenu not found')
        return SubMenuResponse(**Item.__dict__)

    async def get_all(self, menu_id: str, skip: int = 0, limit: int = 100) -> list[SubMenuResponse]:
        stmt = select(SubMenu).filter(SubMenu.menu_id == menu_id).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        submenus = result.scalars().all()
        submenus_list: list[SubMenuResponse] = [SubMenuResponse(**submenu.__dict__) for submenu in submenus]
        return submenus_list

    async def update(self, menu_id: str, submenu_id: str, submenu_data: SubMenuUpdate) -> SubMenuResponse:
        stmt = select(SubMenu).filter(SubMenu.id == submenu_id, SubMenu.menu_id == menu_id)
        result = await self.db.execute(stmt)
        Item: SubMenu = result.scalar()
        if not Item:
            raise HTTPException(status_code=404, detail='submenu not found')

        for key, value in submenu_data.dict(exclude_unset=True).items():
            setattr(Item, key, value)

        await self.db.commit()
        await self.db.refresh(Item)
        return SubMenuResponse(**Item.__dict__)

    async def delete(self, menu_id: str, submenu_id: str):

        stmt = select(SubMenu).filter(SubMenu.id == submenu_id, SubMenu.menu_id == menu_id)
        result = await self.db.execute(stmt)
        Item: SubMenu = result.scalar()

        if not Item:
            return {'status': False, 'message': 'submenu not found'}

        await self.db.delete(Item)
        await self.db.commit()
        return {'status': True, 'message': 'The submenu has been deleted'}
