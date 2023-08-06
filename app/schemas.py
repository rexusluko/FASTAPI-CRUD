from pydantic import BaseModel


class DishBase(BaseModel):
    title: str
    description: str | None = None
    price: str


class DishCreate(DishBase):
    pass


class DishUpdate(DishBase):
    pass


class DishResponse(DishBase):
    id: str

    class Config:
        orm_mode = True


class SubMenuBase(BaseModel):
    title: str
    description: str | None = None


class SubMenuCreate(SubMenuBase):
    pass


class SubMenuUpdate(SubMenuBase):
    pass


class SubMenuResponse(SubMenuBase):
    id: str
    dishes_count: int

    class Config:
        orm_mode = True


class MenuBase(BaseModel):
    title: str
    description: str | None = None


class MenuCreate(MenuBase):
    pass


class MenuUpdate(MenuBase):
    pass


class MenuResponse(MenuBase):
    id: str
    submenus_count: int
    dishes_count: int

    class Config:
        orm_mode = True
