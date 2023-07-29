import uuid

from sqlalchemy import and_
from sqlalchemy.orm import Session

from . import models,schemas


#Menu
def create_menu(db: Session, menu: schemas.MenuCreate):
    db_menu = models.Menu(id=str(uuid.uuid4()), title=menu.title, description=menu.description)
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu

def get_menu(db: Session, menu_id: str):
    return db.query(models.Menu).filter(models.Menu.id == menu_id).first()

def get_menus(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Menu).offset(skip).limit(limit).all()

def update_menu(db: Session, menu_id:str, new_menu: schemas.MenuUpdate):

    db_menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()

    if db_menu:

        db_menu.title = new_menu.title
        db_menu.description = new_menu.description

        db.commit()
    return db_menu

def delete_menu(db: Session,menu_id:str):
    db_menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    if db_menu:
        db.delete(db_menu)
        db.commit()
        return {"status": True, "message": "The menu has been deleted"}
    else:
        return {"status": False, "message": "menu not found"}


#SubMenu
def create_submenu(db: Session, submenu: schemas.SubMenuCreate, menu_id:str):
    db_submenu = models.SubMenu(id=str(uuid.uuid4()), title=submenu.title, description=submenu.description, menu_id=menu_id)
    db.add(db_submenu)
    db.commit()
    db.refresh(db_submenu)
    return db_submenu

def get_submenu(db: Session, menu_id : str,submenu_id: str):
    return db.query(models.SubMenu).filter(and_(models.SubMenu.id == submenu_id,
                                                models.SubMenu.menu_id == menu_id)).first()

def get_submenus(db: Session, menu_id : str,skip: int = 0, limit: int = 100):
    return db.query(models.SubMenu).filter(models.SubMenu.menu_id == menu_id)

def update_submenu(db: Session, menu_id:str, submenu_id:str, new_submenu: schemas.SubMenuUpdate):

    db_submenu = db.query(models.SubMenu).filter(and_(models.SubMenu.id == submenu_id,
                                                      models.SubMenu.menu_id == menu_id)).first()

    if db_submenu:

        db_submenu.title = new_submenu.title
        db_submenu.description = new_submenu.description

        db.commit()
    return db_submenu

def delete_submenu(db: Session,menu_id:str,submenu_id:str):
    db_submenu = db.query(models.SubMenu).filter(and_(models.SubMenu.id == submenu_id,
                                                      models.SubMenu.menu_id == menu_id)).first()
    if db_submenu:
        db.delete(db_submenu)
        db.commit()
        return {"status": True, "message": "The submenu has been deleted"}
    else:
        return {"status": False, "message": "submenu not found"}


#Dish
def create_dish(db: Session, dish: schemas.DishCreate, submenu_id:str):
    price=str(round(float(dish.price), 2))
    db_dish = models.Dish(id=str(uuid.uuid4()), title=dish.title, description=dish.description, price=price, submenu_id=submenu_id)
    db.add(db_dish)
    db.commit()
    db.refresh(db_dish)
    return db_dish

def get_dish(db: Session, submenu_id: str,dish_id:str):
    return db.query(models.Dish).filter(and_(models.Dish.id == dish_id, models.Dish.submenu_id == submenu_id)).first()

def get_dishes(db: Session, submenu_id : str, skip: int = 0, limit: int = 100):
    return db.query(models.Dish).filter(models.Dish.submenu_id == submenu_id)

def update_dish(db: Session, submenu_id:str, dish_id: str, new_dish: schemas.DishUpdate):

    db_dish = db.query(models.Dish).filter(and_(models.Dish.id == dish_id,
                                                models.Dish.submenu_id == submenu_id)).first()

    if db_dish:

        db_dish.title = new_dish.title
        db_dish.description = new_dish.description
        db_dish.price = str(round(float(new_dish.price), 2))

        db.commit()
    return db_dish

def delete_dish(db: Session,submenu_id:str,dish_id:str):
    db_dish = db.query(models.Dish).filter(and_(models.Dish.id == dish_id,
                                                models.Dish.submenu_id == submenu_id)).first()
    if db_dish:
        db.delete(db_dish)
        db.commit()
        return {"status": True, "message": "The dish has been deleted"}
    else:
        return {"status": False, "message": "dish not found"}