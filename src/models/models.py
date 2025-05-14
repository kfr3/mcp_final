from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from .base import BaseModel

# Association tables for many-to-many relationships
recipe_dietary_tags = Table(
    'recipe_dietary_tags',
    BaseModel.metadata,
    Column('recipe_id', Integer, ForeignKey('recipes.id')),
    Column('dietary_tag_id', Integer, ForeignKey('dietary_tags.id'))
)

ingredient_dietary_tags = Table(
    'ingredient_dietary_tags',
    BaseModel.metadata,
    Column('ingredient_id', Integer, ForeignKey('ingredients.id')),
    Column('dietary_tag_id', Integer, ForeignKey('dietary_tags.id'))
)

class Recipe(BaseModel):
    """Recipe model for storing recipe information"""
    __tablename__ = 'recipes'

    name = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    instructions = Column(Text, nullable=False)
    preparation_time = Column(Integer, nullable=False)  # in minutes
    cooking_time = Column(Integer, nullable=False)  # in minutes
    difficulty = Column(String(50), nullable=False)
    servings = Column(Integer, nullable=False)

    # Relationships
    ingredients = relationship('RecipeIngredient', back_populates='recipe')
    dietary_tags = relationship('DietaryTag', secondary=recipe_dietary_tags, back_populates='recipes')

class Ingredient(BaseModel):
    """Ingredient model for storing ingredient information"""
    __tablename__ = 'ingredients'

    name = Column(String(255), nullable=False, index=True)
    category_id = Column(Integer, ForeignKey('ingredient_categories.id'), nullable=False)

    # Relationships
    category = relationship('IngredientCategory', back_populates='ingredients')
    recipes = relationship('RecipeIngredient', back_populates='ingredient')
    dietary_tags = relationship('DietaryTag', secondary=ingredient_dietary_tags, back_populates='ingredients')

class IngredientCategory(BaseModel):
    """Category model for grouping ingredients"""
    __tablename__ = 'ingredient_categories'

    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)

    # Relationships
    ingredients = relationship('Ingredient', back_populates='category')

class DietaryTag(BaseModel):
    """Dietary tag model for storing dietary restrictions and preferences"""
    __tablename__ = 'dietary_tags'

    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)

    # Relationships
    recipes = relationship('Recipe', secondary=recipe_dietary_tags, back_populates='dietary_tags')
    ingredients = relationship('Ingredient', secondary=ingredient_dietary_tags, back_populates='dietary_tags')

class RecipeIngredient(BaseModel):
    """Association model for recipe-ingredient relationships"""
    __tablename__ = 'recipe_ingredients'

    recipe_id = Column(Integer, ForeignKey('recipes.id'), nullable=False)
    ingredient_id = Column(Integer, ForeignKey('ingredients.id'), nullable=False)
    quantity = Column(Float, nullable=False)
    unit = Column(String(50), nullable=False)

    # Relationships
    recipe = relationship('Recipe', back_populates='ingredients')
    ingredient = relationship('Ingredient', back_populates='recipes') 