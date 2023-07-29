def test_get_menus(client, amount: int = None):
    response = client.get(f"/api/v1/menus/")

    assert response.status_code == 200
    if amount:
        assert len(response.json()) == amount


def test_create_menu(client, title: str = "My menu 1", description: str = "My menu description 1"):
    request = {"title": f"{title}", "description": f"{description}"}
    response = client.post("/api/v1/menus", json=request)

    assert response.status_code == 201
    assert "id" in response.json()
    assert response.json()["title"] == request["title"]
    assert response.json()["description"] == request["description"]
    assert response.json()["submenus_count"] == 0
    assert response.json()["dishes_count"] == 0
    return response.json()


def test_get_menu(client, menu_id: str = None, submenus_count: int = None, dishes_count: int = None):
    if not menu_id:
        menu_id = test_create_menu(client)["id"]

    response = client.get(f"/api/v1/menus/{menu_id}/")

    assert response.status_code == 200
    assert "id" in response.json()
    assert "title" in response.json()
    assert "description" in response.json()
    assert "submenus_count" in response.json()
    if submenus_count:
        assert response.json()["submenus_count"] == submenus_count
    assert "dishes_count" in response.json()
    if dishes_count:
        assert response.json()["dishes_count"] == dishes_count


def test_get_non_existing_menu(client, menu_id: str = None):
    response = client.get(f"/api/v1/menus/{menu_id}")

    assert response.status_code == 404
    assert response.json()['detail'] == "menu not found"


def test_update_menu(client, menu_id: str = None, new_title: str = "Changed menu 3",
                     new_description: str = "Changed description 3"):
    if not menu_id:
        menu_id = test_create_menu(client)["id"]
    response = client.patch(f"/api/v1/menus/{menu_id}/", json={"title": f"{new_title}",
                                                               "description": f"{new_description}"})
    assert response.status_code == 200
    assert response.json()["id"] == menu_id
    assert response.json()["title"] == new_title
    assert response.json()["description"] == new_description
    assert "submenus_count" in response.json()
    assert "dishes_count" in response.json()


def test_update_non_existing_menu(client, menu_id: str = None, new_title: str = "Changed menu 3",
                                  new_description: str = "Changed description 3"):
    response = client.patch(f"/api/v1/menus/{menu_id}/", json={"title": f"{new_title}",
                                                               "description": f"{new_description}"})
    assert response.status_code == 404
    assert response.json()['detail'] == "menu not found"


def test_delete_menu(client, menu_id: str = None):
    if not menu_id:
        menu_id = test_create_menu(client)["id"]
    response = client.delete(f"/api/v1/menus/{menu_id}/")
    assert response.status_code == 200
    assert response.json()["status"] == True
    assert response.json()["message"] == "The menu has been deleted"
