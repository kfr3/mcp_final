from typing import List, Optional
from pydantic import BaseModel, Field, validator
from datetime import datetime

from .base import BaseSchema, TimestampMixin

# Ingredient Category Schemas
class IngredientCategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None

class IngredientCategoryCreate(IngredientCategoryBase):
    pass

class IngredientCategoryUpdate(IngredientCategoryBase):
    name: Optional[str] = Field(None, min_length=1, max_length=100)

class IngredientCategory(IngredientCategoryBase, TimestampMixin, BaseSchema):
    id: int

# Dietary Tag Schemas
class DietaryTagBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None

class DietaryTagCreate(DietaryTagBase):
    pass

class DietaryTagUpdate(DietaryTagBase):
    name: Optional[str] = Field(None, min_length=1, max_length=100)

class DietaryTag(DietaryTagBase, TimestampMixin, BaseSchema):
    id: int

# Ingredient Schemas
class IngredientBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    category_id: int

class IngredientCreate(IngredientBase):
    pass

class IngredientUpdate(IngredientBase):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    category_id: Optional[int] = None

class Ingredient(IngredientBase, TimestampMixin, BaseSchema):
    id: int

# Recipe Schemas
class RecipeBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    instructions: str = Field(..., min_length=1)
    preparation_time: int = Field(..., gt=0)
    cooking_time: int = Field(..., gt=0)
    difficulty: str = Field(..., pattern='^(easy|medium|hard)$')
    servings: int = Field(..., gt=0)

    @validator('difficulty')
    def validate_difficulty(cls, v):
        allowed = ['easy', 'medium', 'hard']
        if v.lower() not in allowed:
            raise ValueError(f'Difficulty must be one of {allowed}')
        return v.lower()

class RecipeCreate(RecipeBase):
    pass

class RecipeUpdate(RecipeBase):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    instructions: Optional[str] = Field(None, min_length=1)
    preparation_time: Optional[int] = Field(None, gt=0)
    cooking_time: Optional[int] = Field(None, gt=0)
    difficulty: Optional[str] = Field(None, pattern='^(easy|medium|hard)$')
    servings: Optional[int] = Field(None, gt=0)

class Recipe(RecipeBase, TimestampMixin, BaseSchema):
    id: int

# Recipe Ingredient Schemas
class RecipeIngredientBase(BaseModel):
    recipe_id: int
    ingredient_id: int
    quantity: float = Field(..., gt=0)
    unit: str = Field(..., min_length=1, max_length=50)

class RecipeIngredientCreate(RecipeIngredientBase):
    pass

class RecipeIngredientUpdate(RecipeIngredientBase):
    recipe_id: Optional[int] = None
    ingredient_id: Optional[int] = None
    quantity: Optional[float] = Field(None, gt=0)
    unit: Optional[str] = Field(None, min_length=1, max_length=50)

class RecipeIngredient(RecipeIngredientBase, TimestampMixin, BaseSchema):
    id: int 