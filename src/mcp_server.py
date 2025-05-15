from typing import List, Dict, Optional
from mcp import MCP, Resource, Tool
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database.config import get_db
from database.crud import (
    ingredient_category,
    dietary_tag,
    recipe,
    ingredient,
    recipe_ingredient
)
from tools import find_recipes, suggest_substitutions

# Initialize MCP server
mcp = MCP()

app = mcp.app  # Use the FastAPI instance from MCP

class SubstitutionRequest(BaseModel):
    ingredient: str
    dietary_restrictions: List[str]

@app.get("/ingredients/{category}")
def get_ingredients_by_category(category: str) -> List[str]:
    """
    Get all ingredients in a specific category.
    """
    db = next(get_db())
    category_obj = ingredient_category.get_by_name(db, name=category)
    if not category_obj:
        return []
    
    ingredients = ingredient.get_by_category(db, category_id=category_obj.id)
    return [ing.name for ing in ingredients]

@app.get("/recipe/{recipe_id}")
def get_recipe_details(recipe_id: str) -> Dict:
    """
    Get detailed information about a specific recipe.
    """
    db = next(get_db())
    recipe_obj = recipe.get(db, id=int(recipe_id))
    if not recipe_obj:
        return {}
    
    # Get recipe ingredients
    recipe_ingredients = recipe_ingredient.get_by_recipe(db, recipe_id=recipe_obj.id)
    ingredients_list = []
    for ri in recipe_ingredients:
        ing = ingredient.get(db, id=ri.ingredient_id)
        if ing:
            ingredients_list.append({
                "name": ing.name,
                "quantity": ri.quantity,
                "unit": ri.unit
            })
    
    # Get dietary tags
    dietary_tags = [tag.name for tag in recipe_obj.dietary_tags]
    
    return {
        "id": recipe_obj.id,
        "name": recipe_obj.name,
        "description": recipe_obj.description,
        "instructions": recipe_obj.instructions,
        "preparation_time": recipe_obj.preparation_time,
        "cooking_time": recipe_obj.cooking_time,
        "difficulty": recipe_obj.difficulty,
        "servings": recipe_obj.servings,
        "ingredients": ingredients_list,
        "dietary_tags": dietary_tags
    }

@app.post("/tools/find_recipes")
def find_recipes_tool(
    ingredients: List[str],
    dietary_restrictions: List[str],
    max_cooking_time: Optional[int] = None,
    difficulty_level: Optional[str] = None
) -> List[Dict]:
    """
    Find recipes based on available ingredients and dietary restrictions.
    """
    return find_recipes(
        ingredients=ingredients,
        dietary_restrictions=dietary_restrictions,
        max_cooking_time=max_cooking_time,
        difficulty_level=difficulty_level
    )

@app.post("/tools/suggest_substitutions")
def suggest_substitutions_tool(request: SubstitutionRequest) -> List[Dict]:
    """
    Suggest ingredient substitutions based on dietary restrictions.
    """
    return suggest_substitutions(
        ingredient_name=request.ingredient,
        dietary_restrictions=request.dietary_restrictions
    )

def start_server():
    """
    Start the MCP server.
    """
    mcp.run() 