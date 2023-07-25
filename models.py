from sqlalchemy import Column, ForeignKey, Integer, String,Float
from sqlalchemy.orm import relationship
from database import Base

class Menu(Base):
    __tablename__ = "menus"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)

    submenus = relationship("SubMenu", back_populates="menu",cascade="all, delete-orphan")
    @property
    def submenus_count(self):
        return len(self.submenus)

    @property
    def dishes_count(self):
        return sum(submenu.dishes_count for submenu in self.submenus)


class SubMenu(Base):
    __tablename__ = "submenus"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    menu_id = Column(String, ForeignKey("menus.id"))

    menu = relationship("Menu", back_populates="submenus")
    dishes = relationship("Dish", back_populates="submenu", cascade="all, delete-orphan")

    @property
    def dishes_count(self):
        return len(self.dishes)


class Dish(Base):
    __tablename__ = "dishes"

    id = Column(String, primary_key=True,index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(String,index=True)

    submenu_id = Column(String, ForeignKey("submenus.id"))
    submenu = relationship("SubMenu", back_populates="dishes")