from typing import List, Dict, Optional
from sqlalchemy.orm import Session
import logging

from database.config import get_db
from database.crud import (
    recipe,
    ingredient,
    recipe_ingredient,
    dietary_tag
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def find_recipes(
    ingredients: List[str],
    dietary_restrictions: List[str],
    max_cooking_time: Optional[int] = None,
    difficulty_level: Optional[str] = None,
    db: Optional[Session] = None
) -> List[Dict]:
    """
    Find recipes based on available ingredients and dietary restrictions.
    
    Args:
        ingredients: List of available ingredient names
        dietary_restrictions: List of dietary restrictions to consider
        max_cooking_time: Maximum cooking time in minutes (optional)
        difficulty_level: Recipe difficulty level (easy/medium/hard) (optional)
    
    Returns:
        List of matching recipes with their details
    """
    if db is None:
        db = next(get_db())
    
    # Get all recipes
    recipes_list = recipe.get_multi(db)
    matching_recipes = []
    
    for recipe_obj in recipes_list:
        # Check cooking time
        if max_cooking_time and recipe_obj.cooking_time > max_cooking_time:
            continue
            
        # Check difficulty level
        if difficulty_level and recipe_obj.difficulty != difficulty_level:
            continue
            
        # Check dietary restrictions
        recipe_tags = {tag.name for tag in recipe_obj.dietary_tags}
        if not all(restriction in recipe_tags for restriction in dietary_restrictions):
            continue
            
        # Check ingredients
        recipe_ingredients = recipe_ingredient.get_by_recipe(db, recipe_id=recipe_obj.id)
        recipe_ingredient_names = set()
        for ri in recipe_ingredients:
            ing = ingredient.get(db, id=ri.ingredient_id)
            if ing:
                recipe_ingredient_names.add(ing.name)
        
        # Check if all required ingredients are available
        if all(ing in recipe_ingredient_names for ing in ingredients):
            matching_recipes.append({
                "id": recipe_obj.id,
                "name": recipe_obj.name,
                "description": recipe_obj.description,
                "instructions": recipe_obj.instructions,
                "preparation_time": recipe_obj.preparation_time,
                "cooking_time": recipe_obj.cooking_time,
                "difficulty": recipe_obj.difficulty,
                "servings": recipe_obj.servings,
                "ingredients": [
                    {
                        "name": ing.name,
                        "quantity": ri.quantity,
                        "unit": ri.unit
                    }
                    for ri in recipe_ingredients
                    if (ing := ingredient.get(db, id=ri.ingredient_id))
                ],
                "dietary_tags": [tag.name for tag in recipe_obj.dietary_tags]
            })
    
    return matching_recipes

def suggest_substitutions(
    ingredient_name: str,
    dietary_restrictions: List[str],
    db: Optional[Session] = None
) -> List[Dict]:
    """
    Suggest ingredient substitutions based on dietary restrictions.
    
    Args:
        ingredient_name: Name of the ingredient to substitute
        dietary_restrictions: List of dietary restrictions to consider
    
    Returns:
        List of potential substitute ingredients with their details
    """
    if db is None:
        db = next(get_db())
    # Debug log: Print session identity and list of ingredients
    logger.info("Session ID: %s", id(db))
    all_ingredients = ingredient.get_multi(db)
    logger.info("All ingredients in DB: %s", [ing.name for ing in all_ingredients])
    
    # Return empty list if no dietary restrictions specified
    if not dietary_restrictions:
        logger.warning("No dietary restrictions specified for substitution.")
        return []
    
    # Find the ingredient
    ing = ingredient.get_by_name(db, name=ingredient_name)
    if not ing:
        logger.warning("Ingredient '%s' not found in the database.", ingredient_name)
        return []
    
    # Get all ingredients that match the dietary restrictions
    potential_substitutes = []
    for substitute in all_ingredients:
        if substitute.id == ing.id:
            continue
        substitute_tags = {tag.name for tag in substitute.dietary_tags}
        if all(restriction in substitute_tags for restriction in dietary_restrictions):
            potential_substitutes.append({
                "name": substitute.name,
                "category": substitute.category.name,
                "dietary_tags": [tag.name for tag in substitute.dietary_tags],
                "compatibility_score": calculate_compatibility_score(ing, substitute)
            })
    
    # Sort by compatibility score
    potential_substitutes.sort(key=lambda x: x["compatibility_score"], reverse=True)
    logger.info("Potential substitutes for '%s': %s", ingredient_name, potential_substitutes)
    return potential_substitutes

def calculate_compatibility_score(original: 'Ingredient', substitute: 'Ingredient') -> float:
    """
    Calculate a compatibility score between two ingredients.
    Higher score means better compatibility.
    """
    score = 0.0
    
    # Same category bonus
    if original.category_id == substitute.category_id:
        score += 0.5
    
    # Common dietary tags bonus
    common_tags = set(tag.name for tag in original.dietary_tags) & set(tag.name for tag in substitute.dietary_tags)
    score += len(common_tags) * 0.2
    
    return min(score, 1.0)  # Cap at 1.0 