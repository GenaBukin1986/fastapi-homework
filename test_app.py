from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_create_recipe():
    response = client.post(
        "/recipes",
        json={
            "name": "Омлет",
            "cooking_time": 10,
            "ingredients": {"яйцо": 2, "молоко": 50},
            "description": "Простой омлет на завтрак.",
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Омлет"
    assert data["cooking_time"] == 10
    assert data["ingredients"] == {"яйцо": 2, "молоко": 50}
    assert data["views"] == 0
    assert "id" in data


def test_get_recipes():
    client.post(
        "/recipes",
        json={
            "name": "Блины",
            "cooking_time": 20,
            "ingredients": {"мука": 200, "яйцо": 1},
            "description": "Классические блины.",
        },
    )

    response = client.get("/recipes")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    recipe = data[0]
    assert "name" in recipe
    assert "views" in recipe
    assert "cooking_time" in recipe


def test_get_recipe_increments_views():
    create_response = client.post(
        "/recipes",
        json={
            "name": "Тестовый рецепт",
            "cooking_time": 5,
            "ingredients": {"вода": 100},
            "description": "Тест.",
        },
    )
    recipe_id = create_response.json()["id"]

    response1 = client.get(f"/recipes/{recipe_id}")
    assert response1.status_code == 200
    assert response1.json()["views"] == 1

    response2 = client.get(f"/recipes/{recipe_id}")
    assert response2.json()["views"] == 2
