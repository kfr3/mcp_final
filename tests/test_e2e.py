import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.mcp_server import app
from database.config import get_db
from tests.conftest import test_data

client = TestClient(app)

@pytest.mark.asyncio
async def test_recipe_finding_flow(test_data):
    """Test the complete recipe finding process from start to finish"""
    # Step 1: Get available ingredients
    response = client.get("/ingredients/vegetables")
    assert response.status_code == 200
    available_ingredients = response.json()
    assert isinstance(available_ingredients, list)
    assert "tomato" in available_ingredients

    # Step 2: Find recipes with available ingredients
    payload = {
        "ingredients": ["tomato", "cheese"],
        "dietary_restrictions": ["vegetarian"],
        "max_cooking_time": 15,
        "difficulty_level": "easy"
    }
    response = client.post("/tools/find_recipes", json=payload)
    assert response.status_code == 200
    recipes = response.json()
    assert isinstance(recipes, list)
    assert len(recipes) > 0
    assert any("Tomato and Cheese Salad" in r["name"] for r in recipes)

    # Step 3: Get detailed recipe information
    recipe_id = next(r["id"] for r in recipes if "Tomato and Cheese Salad" in r["name"])
    response = client.get(f"/recipe/{recipe_id}")
    assert response.status_code == 200
    recipe_details = response.json()
    assert recipe_details["name"] == "Tomato and Cheese Salad"
    assert "ingredients" in recipe_details
    assert len(recipe_details["ingredients"]) == 2

    # Step 4: Scale recipe for different servings
    payload = {
        "recipe_id": recipe_id,
        "target_servings": 4
    }
    response = client.post("/tools/scale_recipe", json=payload)
    assert response.status_code == 200
    scaled_recipe = response.json()
    assert scaled_recipe["target_servings"] == 4
    assert scaled_recipe["scaling_factor"] == 2.0
    assert len(scaled_recipe["ingredients"]) == 2
    assert scaled_recipe["ingredients"][0]["quantity"] == 4  # 2 tomatoes * 2
    assert scaled_recipe["ingredients"][1]["quantity"] == 200  # 100g cheese * 2

@pytest.mark.asyncio
async def test_ingredient_substitution_flow(test_data):
    """Test the complete ingredient substitution process from start to finish"""
    # Step 1: Get ingredient categories
    response = client.get("/categories/all")
    assert response.status_code == 200
    categories = response.json()
    assert isinstance(categories, list)
    assert "dairy" in categories

    # Step 2: Get ingredients in a category
    response = client.get("/ingredients/dairy")
    assert response.status_code == 200
    dairy_ingredients = response.json()
    assert isinstance(dairy_ingredients, list)
    assert "cheese" in dairy_ingredients

    # Step 3: Request substitutions for an ingredient
    payload = {
        "ingredient": "cheese",
        "dietary_restrictions": ["vegan"]
    }
    response = client.post("/tools/suggest_substitutions", json=payload)
    assert response.status_code == 200
    substitutions = response.json()
    assert isinstance(substitutions, list)
    assert len(substitutions) > 0
    assert all("vegan" in sub["dietary_tags"] for sub in substitutions)

    # Step 4: Verify substitution compatibility
    if substitutions:
        substitute = substitutions[0]
        assert "name" in substitute
        assert "category" in substitute
        assert "dietary_tags" in substitute
        assert "compatibility_score" in substitute
        assert substitute["compatibility_score"] > 0

    # Step 5: Test multiple dietary restrictions
    payload = {
        "ingredient": "cheese",
        "dietary_restrictions": ["vegan", "gluten-free"]
    }
    response = client.post("/tools/suggest_substitutions", json=payload)
    assert response.status_code == 200
    multi_substitutions = response.json()
    assert isinstance(multi_substitutions, list)
    assert all(all(tag in sub["dietary_tags"] for tag in ["vegan", "gluten-free"]) 
              for sub in multi_substitutions) 