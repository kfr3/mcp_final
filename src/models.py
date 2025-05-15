from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

# Create base class
Base = declarative_base()

# Association tables
recipe_dietary_tags = Table(
    'recipe_dietary_tags',
    Base.metadata,
    Column('recipe_id', Integer, ForeignKey('recipes.id'), primary_key=True),
    Column('dietary_tag_id', Integer, ForeignKey('dietary_tags.id'), primary_key=True)
)

ingredient_dietary_tags = Table(
    'ingredient_dietary_tags',
    Base.metadata,
    Column('ingredient_id', Integer, ForeignKey('ingredients.id'), primary_key=True),
    Column('dietary_tag_id', Integer, ForeignKey('dietary_tags.id'), primary_key=True)
)

class IngredientCategory(Base):
    __tablename__ = "ingredient_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    ingredients = relationship("Ingredient", back_populates="category")

class DietaryTag(Base):
    __tablename__ = "dietary_tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    recipes = relationship("Recipe", secondary=recipe_dietary_tags, back_populates="dietary_tags")
    ingredients = relationship("Ingredient", secondary=ingredient_dietary_tags, back_populates="dietary_tags")

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    instructions = Column(Text, nullable=False)
    preparation_time = Column(Integer, nullable=False)
    cooking_time = Column(Integer, nullable=False)
    difficulty = Column(String(50), nullable=False)
    servings = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    ingredients = relationship("RecipeIngredient", back_populates="recipe")
    dietary_tags = relationship("DietaryTag", secondary=recipe_dietary_tags, back_populates="recipes")

class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True, index=True)
    category_id = Column(Integer, ForeignKey("ingredient_categories.id"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    category = relationship("IngredientCategory", back_populates="ingredients")
    recipes = relationship("RecipeIngredient", back_populates="ingredient")
    dietary_tags = relationship("DietaryTag", secondary=ingredient_dietary_tags, back_populates="ingredients")

class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredients"

    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), nullable=False)
    quantity = Column(Float, nullable=False)
    unit = Column(String(50), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    recipe = relationship("Recipe", back_populates="ingredients")
    ingredient = relationship("Ingredient", back_populates="recipes") 