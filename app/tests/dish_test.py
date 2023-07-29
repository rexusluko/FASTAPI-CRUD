from .menu_test import test_create_menu
from .submenu_test import test_create_submenu


def test_get_dishes(client, menu_id: str = None, submenu_id: str = None, amount: int = 0):
    if not menu_id:
        menu_id = test_create_menu(client)["id"]
    if not submenu_id:
        submenu_id = test_create_submenu(client, menu_id=menu_id)["id"]
    response = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes")

    assert response.status_code == 200
    assert len(response.json()) == amount


def test_create_dish(client, menu_id: str = None, submenu_id: str = None, title: str = "My dish 1",
                     description: str = "My dish description 1", price: str = "0.0"):
    if not menu_id:
        menu_id = test_create_menu(client)["id"]
    if not submenu_id:
        submenu_id = test_create_submenu(client,menu_id=menu_id)["id"]
    request = {"title": f"{title}", "description": f"{description}", "price": f"{price}"}
    response = client.post(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", json=request)

    assert response.status_code == 201
    assert "id" in response.json()
    assert response.json()["title"] == request["title"]
    assert response.json()["description"] == request["description"]
    assert response.json()["price"] == request["price"]
    return response.json()


def test_get_dish(client, menu_id: str = None, submenu_id: str = None, dish_id: str = None):
    if not menu_id:
        menu_id = test_create_menu(client)["id"]
    if not submenu_id:
        submenu_id = test_create_submenu(client,menu_id=menu_id)["id"]
    if not dish_id:
        dish_id = test_create_dish(client,menu_id=menu_id,submenu_id=submenu_id)["id"]

    response = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")

    assert response.status_code == 200
    assert "id" in response.json()
    assert "title" in response.json()
    assert "description" in response.json()
    assert "price" in response.json()


def test_get_non_existing_dish(client, menu_id: str = None, submenu_id: str = None, dish_id: str = None):
    if not menu_id:
        menu_id = test_create_menu(client)["id"]
    if not submenu_id:
        submenu_id = test_create_submenu(client,menu_id=menu_id)["id"]
    response = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")

    assert response.status_code == 404
    assert response.json()['detail'] == "dish not found"


def test_update_dish(client, menu_id: str = None, submenu_id: str = None, dish_id: str = None,
                     new_title: str = "Changed menu 4",
                     new_description: str = "Changed description 4", new_price: str = "4.4"):
    if not menu_id:
        menu_id = test_create_menu(client)["id"]
    if not submenu_id:
        submenu_id = test_create_submenu(client,menu_id=menu_id)["id"]
    if not dish_id:
        dish_id = test_create_dish(client,menu_id=menu_id,submenu_id=submenu_id)["id"]

    request = {"title": f"{new_title}", "description": f"{new_description}", "price": f"{new_price}"}
    response = client.patch(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", json=request)

    assert response.status_code == 200
    assert response.json()["id"] == dish_id
    assert response.json()["title"] == new_title
    assert response.json()["description"] == new_description
    assert response.json()["price"] == new_price


def test_update_non_existing_dish(client, menu_id: str = None, submenu_id: str = None, dish_id: str = None,
                                  new_title: str = "Changed menu 5",
                                  new_description: str = "Changed description 5",
                                  new_price: str = "5.5"):
    if not menu_id:
        menu_id = test_create_menu(client)["id"]
    if not submenu_id:
        submenu_id = test_create_submenu(client,menu_id=menu_id)["id"]
    response = client.patch(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
                            json={"title": f"{new_title}",
                                  "description": f"{new_description}",
                                  "price": f"{new_price}"})
    assert response.status_code == 404
    assert response.json()['detail'] == "dish not found"


def test_delete_dish(client, menu_id: str = None, submenu_id: str = None, dish_id: str = None):
    if not menu_id:
        menu_id = test_create_menu(client)["id"]
    if not submenu_id:
        submenu_id = test_create_submenu(client,menu_id=menu_id)["id"]
    if not dish_id:
        dish_id = test_create_dish(client,menu_id=menu_id,submenu_id=submenu_id)["id"]
    response = client.delete(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")

    assert response.status_code == 200
    assert response.json()["status"] == True
    assert response.json()["message"] == "The dish has been deleted"
