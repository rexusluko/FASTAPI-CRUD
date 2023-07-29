from . import menu_test, submenu_test, dish_test


def test_count(client):
    menu_test.test_get_menus(client)  # Просмотр списка меню
    menu_id = menu_test.test_create_menu(client, title="menu 1", description="descrition 1")["id"]  # Создание меню
    menu_test.test_get_menu(client, menu_id)  # Просмотр меню 1
    menu_test.test_get_menus(client, amount=1)  # Просмотр списка меню
    submenu_test.test_get_submenus(client, menu_id=menu_id)  # Просмотр списка подменю у меню 1
    submenu1_id = submenu_test.test_create_submenu(client, menu_id=menu_id, title="submenu 1")["id"]  # Создание подменю 1 в меню
    submenu2_id = submenu_test.test_create_submenu(client, menu_id=menu_id, title="submenu 2")["id"]  # Создание подменю 2 в меню
    submenu_test.test_get_submenus(client, menu_id=menu_id, amount=2)  # Просмотр списка подменю у меню 1
    dish_test.test_get_dishes(client, menu_id=menu_id, submenu_id=submenu1_id)  # Просмотр списка блюд у подменю 1
    dish1_id = dish_test.test_create_dish(client, menu_id=menu_id, submenu_id=submenu1_id,title="dish 1")  # Создание блюда 1 в подменю 1
    dish2_id = dish_test.test_create_dish(client, menu_id=menu_id, submenu_id=submenu1_id, title="dish 2")  # Создание блюда 2 в подменю 1
    dish_test.test_get_dishes(client, menu_id=menu_id, submenu_id=submenu1_id, amount=2)  # Просмотр списка блюд у подменю 1
    menu_test.test_get_menu(client,menu_id=menu_id,submenus_count=2,dishes_count=2) # Проверка числа подменю и блюд у меню
    dish_test.test_get_dishes(client, menu_id=menu_id, submenu_id=submenu2_id)  # Просмотр списка блюд у подменю 2
    dish3_id = dish_test.test_create_dish(client, menu_id=menu_id, submenu_id=submenu2_id,title="dish 3")  # Создание блюда 3 в подменю 2
    dish_test.test_get_dishes(client, menu_id=menu_id, submenu_id=submenu2_id, amount=1)  # Просмотр списка блюд у подменю 2
    menu_test.test_get_menu(client,menu_id=menu_id,submenus_count=2,dishes_count=3) # Проверка числа подменю и блюд у меню
    submenu_test.test_delete_submenu(client,menu_id=menu_id,submenu_id=submenu1_id)# Удаление подменю 1
    menu_test.test_get_menu(client,menu_id=menu_id,submenus_count=1,dishes_count=1) # Проверка числа подменю и блюд у меню
    dish_test.test_get_non_existing_dish(client,menu_id=menu_id,submenu_id=submenu1_id,dish_id=dish1_id)# Попытка просмотреть удалённое блюдо
    submenu_test.test_get_non_existing_submenu(client,menu_id=menu_id,submenu_id=submenu1_id)# Попытка просмотреть удалённое подменю
    menu_test.test_delete_menu(client,menu_id=menu_id)# Удаление меню
    menu_test.test_get_menus(client)  # Просмотр списка меню
    dish_test.test_get_non_existing_dish(client, menu_id=menu_id, submenu_id=submenu2_id,
                                         dish_id=dish3_id)  # Попытка просмотреть удалённое блюдо




