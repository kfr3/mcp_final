import pytest
from fastapi.testclient import TestClient
from src.mcp_server import app
from src.database.config import get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def override_get_db(test_data, db_session):
    def _get_db_override():
        yield db_session
    app.dependency_overrides[get_db] = _get_db_override
    yield
    app.dependency_overrides.clear()


def test_get_ingredients_by_category(test_data):
    # Use a known category from test_data
    category = "vegetables"
    response = client.get(f"/ingredients/{category}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any("tomato" in ing.lower() for ing in data)


def test_get_recipe_details(test_data):
    # Use a known recipe from test_data
    recipe_id = test_data["recipes"]["salad"].id
    response = client.get(f"/recipe/{recipe_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Tomato and Cheese Salad"
    assert "ingredients" in data


def test_find_recipes(test_data):
    payload = {
        "ingredients": ["tomato", "cheese"],
        "dietary_restrictions": ["vegetarian"],
        "max_cooking_time": 15,
        "difficulty_level": "easy"
    }
    response = client.post("/tools/find_recipes", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any("Tomato and Cheese Salad" in r["name"] for r in data)


def test_suggest_substitutions(test_data):
    # Test case 1: Basic substitution for vegan cheese
    payload = {
        "ingredient": "cheese",
        "dietary_restrictions": ["vegan"]
    }
    response = client.post("/tools/suggest_substitutions", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # Should suggest at least one vegan-compatible substitution
    assert any("vegan" in sub["dietary_tags"] for sub in data)
    
    # Test case 2: Substitution for gluten-free ingredient
    payload = {
        "ingredient": "salt",
        "dietary_restrictions": ["gluten-free"]
    }
    response = client.post("/tools/suggest_substitutions", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert all("gluten-free" in sub["dietary_tags"] for sub in data)
    
    # Test case 3: Multiple dietary restrictions
    payload = {
        "ingredient": "tomato",
        "dietary_restrictions": ["vegan", "gluten-free"]
    }
    response = client.post("/tools/suggest_substitutions", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all(all(tag in sub["dietary_tags"] for tag in ["vegan", "gluten-free"]) for sub in data)
    
    # Test case 4: Non-existent ingredient
    payload = {
        "ingredient": "nonexistent_ingredient",
        "dietary_restrictions": ["vegetarian"]
    }
    response = client.post("/tools/suggest_substitutions", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0
    
    # Test case 5: No dietary restrictions
    payload = {
        "ingredient": "cheese",
        "dietary_restrictions": []
    }
    response = client.post("/tools/suggest_substitutions", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0  # Should return empty list when no restrictions specified 