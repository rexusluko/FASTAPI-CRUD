from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session


import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/v1/menus", response_model=schemas.Menu,status_code=201)
def create_menu(menu: schemas.MenuCreate, db: Session = Depends(get_db)):
    return crud.create_menu(db=db, menu=menu)


@app.get("/api/v1/menus", response_model=list[schemas.Menu])
def read_menus(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    menus = crud.get_menus(db, skip=skip, limit=limit)
    return menus


@app.get("/api/v1/menus/{menu_id}", response_model=schemas.Menu)
def read_menu(menu_id: str, db: Session = Depends(get_db)):
    db_menu = crud.get_menu(db, menu_id=menu_id)
    if db_menu is None:
        raise HTTPException(status_code=404, detail="menu not found")
    return db_menu

@app.patch("/api/v1/menus/{menu_id}", response_model=schemas.SubMenu)
def update_menu(menu_id:str,new_menu: schemas.MenuUpdate,db: Session = Depends(get_db)):
    db_menu=crud.update_menu(db,menu_id=menu_id,new_menu=new_menu)
    if db_menu is None:
        raise HTTPException(status_code=404, detail="menu not found")
    return db_menu

@app.delete("/api/v1/menus/{menu_id}")
def delete_menu(menu_id:str,db : Session = Depends(get_db)):
    return crud.delete_menu(db,menu_id=menu_id)


@app.post("/api/v1/menus/{menu_id}/submenus", response_model=schemas.SubMenu,status_code=201)
def create_submenu(
    menu_id: str, submenu: schemas.SubMenuCreate, db: Session = Depends(get_db)
):
    return crud.create_submenu(db=db, submenu=submenu, menu_id=menu_id)


@app.get("/api/v1/menus/{menu_id}/submenus", response_model=list[schemas.SubMenu])
def read_submenus(menu_id:str , skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    submenus = crud.get_submenus(db, menu_id=menu_id,skip=skip, limit=limit)
    return submenus

@app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}", response_model=schemas.SubMenu)
def read_submenu(menu_id:str , submenu_id:str,db: Session = Depends(get_db)):
    db_submenu=crud.get_submenu(db,menu_id=menu_id,submenu_id=submenu_id)
    if db_submenu is None:
        raise HTTPException(status_code=404, detail="submenu not found")
    return db_submenu

@app.patch("/api/v1/menus/{menu_id}/submenus/{submenu_id}", response_model=schemas.SubMenu)
def update_submenu(menu_id:str,submenu_id:str,new_submenu: schemas.SubMenuUpdate,db: Session = Depends(get_db)):
    db_submenu=crud.update_submenu(db,menu_id=menu_id,submenu_id=submenu_id,new_submenu=new_submenu)
    if db_submenu is None:
        raise HTTPException(status_code=404, detail="submenu not found")
    return db_submenu

@app.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
def delete_submenu(menu_id:str,submenu_id:str,db : Session = Depends(get_db)):
    return crud.delete_submenu(db,menu_id=menu_id,submenu_id=submenu_id)


@app.post("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", response_model=schemas.Dish,status_code=201)
def create_dish(
    submenu_id: str, dish: schemas.DishCreate, db: Session = Depends(get_db)
):
    return crud.create_dish(db=db, dish=dish,submenu_id=submenu_id)

@app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", response_model=list[schemas.Dish])
def read_dishes(submenu_id:str,skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    dishes = crud.get_dishes(db,submenu_id=submenu_id,skip=skip, limit=limit)
    return dishes

@app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=schemas.Dish)
def read_dish(submenu_id:str,dish_id:str,db: Session = Depends(get_db)):
    db_dish=crud.get_dish(db,submenu_id=submenu_id,dish_id=dish_id)
    if db_dish is None:
        raise HTTPException(status_code=404, detail="dish not found")
    return db_dish

@app.patch("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=schemas.Dish)
def update_dish(submenu_id:str,dish_id:str,new_dish: schemas.DishUpdate,db: Session = Depends(get_db)):
    db_dish=crud.update_dish(db,submenu_id=submenu_id,dish_id=dish_id,new_dish=new_dish)
    if db_dish is None:
        raise HTTPException(status_code=404, detail="dish not found")
    return db_dish

@app.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
def delete_dish(submenu_id:str,dish_id:str,db : Session = Depends(get_db)):
    return crud.delete_dish(db,submenu_id=submenu_id,dish_id=dish_id)

