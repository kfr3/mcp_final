from typing import List, Dict, Optional, Set, Tuple
from sqlalchemy.orm import Session
from dataclasses import dataclass
from enum import Enum

from src.database.config import get_db
from src.database.crud import (
    recipe,
    ingredient,
    recipe_ingredient,
    dietary_tag
)

class DifficultyLevel(Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

@dataclass
class RecipeMatch:
    recipe_id: int
    match_score: float
    missing_ingredients: List[str]
    matching_ingredients: List[str]
    dietary_compatibility: float

class RecipeMatcher:
    def __init__(self, db: Session):
        self.db = db

    def find_matches(
        self,
        available_ingredients: List[str],
        dietary_restrictions: List[str],
        max_cooking_time: Optional[int] = None,
        difficulty_level: Optional[str] = None
    ) -> List[RecipeMatch]:
        """
        Find recipes that match the given criteria with a scoring system.
        """
        recipes = recipe.get_multi(self.db)
        matches = []

        for recipe_obj in recipes:
            # Skip if cooking time exceeds limit
            if max_cooking_time and recipe_obj.cooking_time > max_cooking_time:
                continue

            # Skip if difficulty doesn't match
            if difficulty_level and recipe_obj.difficulty != difficulty_level:
                continue

            # Get recipe ingredients
            recipe_ingredients = recipe_ingredient.get_by_recipe(self.db, recipe_id=recipe_obj.id)
            recipe_ingredient_names = set()
            for ri in recipe_ingredients:
                ing = ingredient.get(self.db, id=ri.ingredient_id)
                if ing:
                    recipe_ingredient_names.add(ing.name)

            # Calculate ingredient match
            available_set = set(available_ingredients)
            matching = available_set & recipe_ingredient_names
            missing = recipe_ingredient_names - available_set

            # Calculate match score
            match_score = len(matching) / len(recipe_ingredient_names) if recipe_ingredient_names else 0

            # Calculate dietary compatibility
            recipe_tags = {tag.name for tag in recipe_obj.dietary_tags}
            dietary_compatibility = len(set(dietary_restrictions) & recipe_tags) / len(dietary_restrictions) if dietary_restrictions else 1.0

            matches.append(RecipeMatch(
                recipe_id=recipe_obj.id,
                match_score=match_score,
                missing_ingredients=list(missing),
                matching_ingredients=list(matching),
                dietary_compatibility=dietary_compatibility
            ))

        # Sort by match score and dietary compatibility
        matches.sort(key=lambda x: (x.match_score, x.dietary_compatibility), reverse=True)
        return matches

class IngredientCompatibilityChecker:
    def __init__(self, db: Session):
        self.db = db

    def check_compatibility(self, ingredient1: str, ingredient2: str) -> Tuple[float, List[str]]:
        """
        Check compatibility between two ingredients and return a score and reasons.
        """
        ing1 = ingredient.get_by_name(self.db, name=ingredient1)
        ing2 = ingredient.get_by_name(self.db, name=ingredient2)

        if not ing1 or not ing2:
            return 0.0, ["One or both ingredients not found"]

        score = 0.0
        reasons = []

        # Check category compatibility
        if ing1.category_id == ing2.category_id:
            score += 0.5
            reasons.append("Same ingredient category")

        # Check dietary tag compatibility
        ing1_tags = {tag.name for tag in ing1.dietary_tags}
        ing2_tags = {tag.name for tag in ing2.dietary_tags}
        common_tags = ing1_tags & ing2_tags
        if common_tags:
            score += len(common_tags) * 0.2
            reasons.append(f"Common dietary tags: {', '.join(common_tags)}")

        return min(score, 1.0), reasons

class DietaryRestrictionValidator:
    def __init__(self, db: Session):
        self.db = db

    def validate_recipe(
        self,
        recipe_id: int,
        dietary_restrictions: List[str]
    ) -> Tuple[bool, List[str]]:
        """
        Validate if a recipe meets all dietary restrictions.
        """
        recipe_obj = recipe.get(self.db, id=recipe_id)
        if not recipe_obj:
            return False, ["Recipe not found"]

        recipe_tags = {tag.name for tag in recipe_obj.dietary_tags}
        missing_restrictions = set(dietary_restrictions) - recipe_tags

        if missing_restrictions:
            return False, [f"Missing dietary restrictions: {', '.join(missing_restrictions)}"]

        return True, ["Recipe meets all dietary restrictions"]

    def validate_ingredients(
        self,
        ingredients: List[str],
        dietary_restrictions: List[str]
    ) -> Tuple[bool, List[str]]:
        """
        Validate if all ingredients meet the dietary restrictions.
        """
        invalid_ingredients = []
        for ing_name in ingredients:
            ing = ingredient.get_by_name(self.db, name=ing_name)
            if not ing:
                invalid_ingredients.append(f"Ingredient not found: {ing_name}")
                continue

            ing_tags = {tag.name for tag in ing.dietary_tags}
            missing_restrictions = set(dietary_restrictions) - ing_tags
            if missing_restrictions:
                invalid_ingredients.append(
                    f"{ing_name} missing restrictions: {', '.join(missing_restrictions)}"
                )

        return len(invalid_ingredients) == 0, invalid_ingredients

class RecipeScaler:
    def __init__(self, db: Session):
        self.db = db

    def scale_recipe(
        self,
        recipe_id: int,
        target_servings: int
    ) -> Dict:
        """
        Scale a recipe's ingredients to match the target number of servings.
        """
        recipe_obj = recipe.get(self.db, id=recipe_id)
        if not recipe_obj:
            return {}

        # Calculate scaling factor
        scaling_factor = target_servings / recipe_obj.servings

        # Get and scale ingredients
        recipe_ingredients = recipe_ingredient.get_by_recipe(self.db, recipe_id=recipe_obj.id)
        scaled_ingredients = []
        for ri in recipe_ingredients:
            ing = ingredient.get(self.db, id=ri.ingredient_id)
            if ing:
                scaled_ingredients.append({
                    "name": ing.name,
                    "quantity": ri.quantity * scaling_factor,
                    "unit": ri.unit
                })

        return {
            "id": recipe_obj.id,
            "name": recipe_obj.name,
            "original_servings": recipe_obj.servings,
            "target_servings": target_servings,
            "scaling_factor": scaling_factor,
            "ingredients": scaled_ingredients,
            "instructions": recipe_obj.instructions,
            "preparation_time": recipe_obj.preparation_time,
            "cooking_time": recipe_obj.cooking_time
        } 