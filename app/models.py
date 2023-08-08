from sqlalchemy import Column, ForeignKey, String, func, select
from sqlalchemy.orm import column_property, relationship

from .database import Base


class Dish(Base):
    __tablename__ = 'dishes'

    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(String, index=True)

    submenu_id = Column(String, ForeignKey('submenus.id', ondelete='CASCADE'))
    submenu = relationship('SubMenu', back_populates='dishes')


class SubMenu(Base):
    __tablename__ = 'submenus'

    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    menu_id = Column(String, ForeignKey('menus.id', ondelete='CASCADE'))

    menu = relationship('Menu', back_populates='submenus')
    dishes = relationship('Dish', back_populates='submenu', cascade='all, delete-orphan')

    dishes_count = column_property(
        select(func.count(Dish.id)).where(Dish.submenu_id == id).correlate_except(Dish).as_scalar()
    )


class Menu(Base):
    __tablename__ = 'menus'

    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)

    submenus = relationship('SubMenu', back_populates='menu', cascade='all, delete-orphan')

    submenus_count = column_property(
        select(func.count(SubMenu.id)).where(SubMenu.menu_id == id).correlate_except(SubMenu).as_scalar()
    )

    dishes_count = column_property(
        select(func.count(Dish.id)).where(Dish.submenu_id.in_(
            select(SubMenu.id).where(SubMenu.menu_id == id)
        )).correlate_except(Dish).as_scalar()
    )
