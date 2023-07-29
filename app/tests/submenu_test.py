from .menu_test import test_create_menu


def test_get_submenus(client, menu_id: str = None, amount: int = 0):
    if not menu_id:
        menu_id = test_create_menu(client)["id"]
    response = client.get(f"/api/v1/menus/{menu_id}/submenus")

    assert response.status_code == 200
    assert len(response.json()) == amount


def test_create_submenu(client, menu_id: str = None, title: str = "My submenu 1",
                        description: str = "My submenu description 1"):
    if not menu_id:
        menu_id = test_create_menu(client)["id"]

    request = {"title": f"{title}", "description": f"{description}"}
    response = client.post(f"/api/v1/menus/{menu_id}/submenus", json=request)

    assert response.status_code == 201
    assert "id" in response.json()
    assert response.json()["title"] == request["title"]
    assert response.json()["description"] == request["description"]
    assert response.json()["dishes_count"] == 0
    return response.json()


def test_get_submenu(client, menu_id: str = None, submenu_id: str = None, dishes_count: int = None):
    if not menu_id:
        menu_id = test_create_menu(client)["id"]
    if not submenu_id:
        submenu_id = test_create_submenu(client, menu_id=menu_id)["id"]

    response = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")

    assert response.status_code == 200
    assert "id" in response.json()
    assert "title" in response.json()
    assert "description" in response.json()
    assert "dishes_count" in response.json()
    if dishes_count:
        assert response.json()["dishes_count"] == dishes_count


def test_get_non_existing_submenu(client, menu_id: str = None, submenu_id: str = None):
    if not menu_id:
        menu_id = test_create_menu(client)["id"]

    response = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")

    assert response.status_code == 404
    assert response.json()['detail'] == "submenu not found"


def test_update_submenu(client, menu_id: str = None, submenu_id: str = None, new_title: str = "Changed menu 3",
                        new_description: str = "Changed description 3"):
    if not menu_id:
        menu_id = test_create_menu(client)["id"]
    if not submenu_id:
        submenu_id = test_create_submenu(client, menu_id=menu_id)["id"]
    response = client.patch(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}", json={"title": f"{new_title}",
                                                                                    "description": f"{new_description}"})
    assert response.status_code == 200
    assert response.json()["id"] == submenu_id
    assert response.json()["title"] == new_title
    assert response.json()["description"] == new_description
    assert "dishes_count" in response.json()


def test_update_non_existing_submenu(client, menu_id: str = None, submenu_id: str = None,
                                     new_title: str = "Changed menu 3",
                                     new_description: str = "Changed description 3"):
    if not menu_id:
        menu_id = test_create_menu(client)["id"]
    response = client.patch(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}", json={"title": f"{new_title}",
                                                                                    "description": f"{new_description}"})
    assert response.status_code == 404
    assert response.json()['detail'] == "submenu not found"


def test_delete_submenu(client, menu_id: str = None, submenu_id: str = None):
    if not menu_id:
        menu_id = test_create_menu(client)["id"]
    if not submenu_id:
        submenu_id = test_create_submenu(client, menu_id=menu_id)["id"]
    response = client.delete(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    assert response.status_code == 200
    assert response.json()["status"] == True
    assert response.json()["message"] == "The submenu has been deleted"
