from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_

from .crud_base import CRUDBase
from src.models import (
    Recipe,
    Ingredient,
    RecipeIngredient,
    DietaryTag,
    IngredientCategory
)
from src.schemas.models import (
    IngredientCategoryCreate, IngredientCategoryUpdate,
    DietaryTagCreate, DietaryTagUpdate,
    RecipeCreate, RecipeUpdate,
    IngredientCreate, IngredientUpdate,
    RecipeIngredientCreate, RecipeIngredientUpdate
)

class CRUDIngredientCategory(CRUDBase[IngredientCategory, IngredientCategoryCreate, IngredientCategoryUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[IngredientCategory]:
        return db.query(self.model).filter(self.model.name == name).first()

class CRUDDietaryTag(CRUDBase[DietaryTag, DietaryTagCreate, DietaryTagUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[DietaryTag]:
        return db.query(self.model).filter(self.model.name == name).first()

class CRUDRecipe(CRUDBase[Recipe, RecipeCreate, RecipeUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Recipe]:
        return db.query(self.model).filter(self.model.name == name).first()

    def get_by_difficulty(self, db: Session, *, difficulty: str) -> List[Recipe]:
        return db.query(self.model).filter(self.model.difficulty == difficulty).all()

    def get_by_cooking_time(self, db: Session, *, max_time: int) -> List[Recipe]:
        return db.query(self.model).filter(self.model.cooking_time <= max_time).all()

class CRUDIngredient(CRUDBase[Ingredient, IngredientCreate, IngredientUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Ingredient]:
        return db.query(self.model).filter(self.model.name == name).first()

    def get_by_category(self, db: Session, *, category_id: int) -> List[Ingredient]:
        return db.query(self.model).filter(self.model.category_id == category_id).all()

class CRUDRecipeIngredient(CRUDBase[RecipeIngredient, RecipeIngredientCreate, RecipeIngredientUpdate]):
    def get_by_recipe(self, db: Session, *, recipe_id: int) -> List[RecipeIngredient]:
        return db.query(self.model).filter(self.model.recipe_id == recipe_id).all()

    def get_by_ingredient(self, db: Session, *, ingredient_id: int) -> List[RecipeIngredient]:
        return db.query(self.model).filter(self.model.ingredient_id == ingredient_id).all()

    def get_by_recipe_and_ingredient(
        self, db: Session, *, recipe_id: int, ingredient_id: int
    ) -> Optional[RecipeIngredient]:
        return db.query(self.model).filter(
            and_(
                self.model.recipe_id == recipe_id,
                self.model.ingredient_id == ingredient_id
            )
        ).first()

# Create instances for use in the application
ingredient_category = CRUDIngredientCategory(IngredientCategory)
dietary_tag = CRUDDietaryTag(DietaryTag)
recipe = CRUDRecipe(Recipe)
ingredient = CRUDIngredient(Ingredient)
recipe_ingredient = CRUDRecipeIngredient(RecipeIngredient) 