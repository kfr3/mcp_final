import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models import (
    Recipe,
    Ingredient,
    RecipeIngredient,
    DietaryTag,
    IngredientCategory,
    Base
)

@pytest.fixture(scope="function")
def engine():
    """Create a test database engine"""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    return engine

@pytest.fixture(scope="function")
def SessionLocal(engine):
    """Create a test database session factory"""
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session(engine, SessionLocal):
    """Create a test database session"""
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionLocal(bind=connection)
    
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="function")
def test_data(db_session):
    """Create test data for all tests"""
    # Create categories
    categories = {}
    for name in ["vegetables", "dairy", "meat", "spices"]:
        category = IngredientCategory(name=name)
        db_session.add(category)
        db_session.commit()
        categories[name] = category

    # Create dietary tags
    tags = {}
    for name in ["vegetarian", "vegan", "gluten-free", "dairy-free"]:
        tag = DietaryTag(name=name)
        db_session.add(tag)
        db_session.commit()
        tags[name] = tag

    # Create ingredients
    ingredients = {
        "tomato": Ingredient(
            name="tomato",
            category_id=categories["vegetables"].id,
            dietary_tags=[tags["vegetarian"], tags["vegan"], tags["gluten-free"]]
        ),
        "cheese": Ingredient(
            name="cheese",
            category_id=categories["dairy"].id,
            dietary_tags=[tags["vegetarian"], tags["gluten-free"]]
        ),
        "chicken": Ingredient(
            name="chicken",
            category_id=categories["meat"].id,
            dietary_tags=[tags["gluten-free"]]
        ),
        "salt": Ingredient(
            name="salt",
            category_id=categories["spices"].id,
            dietary_tags=[tags["vegetarian"], tags["vegan"], tags["gluten-free"], tags["dairy-free"]]
        )
    }
    db_session.add_all(ingredients.values())
    db_session.commit()

    # Create recipes
    recipes = {
        "salad": Recipe(
            name="Tomato and Cheese Salad",
            description="Simple salad with tomatoes and cheese",
            instructions="1. Slice tomatoes\n2. Add cheese\n3. Serve",
            preparation_time=10,
            cooking_time=0,
            difficulty="easy",
            servings=2,
            dietary_tags=[tags["vegetarian"], tags["gluten-free"]]
        ),
        "chicken_dish": Recipe(
            name="Chicken with Salt",
            description="Simple chicken dish",
            instructions="1. Season chicken\n2. Cook\n3. Serve",
            preparation_time=15,
            cooking_time=30,
            difficulty="medium",
            servings=4,
            dietary_tags=[tags["gluten-free"]]
        )
    }
    db_session.add_all(recipes.values())
    db_session.commit()

    # Add recipe ingredients
    recipe_ingredients = [
        RecipeIngredient(
            recipe_id=recipes["salad"].id,
            ingredient_id=ingredients["tomato"].id,
            quantity=2,
            unit="pieces"
        ),
        RecipeIngredient(
            recipe_id=recipes["salad"].id,
            ingredient_id=ingredients["cheese"].id,
            quantity=100,
            unit="g"
        ),
        RecipeIngredient(
            recipe_id=recipes["chicken_dish"].id,
            ingredient_id=ingredients["chicken"].id,
            quantity=500,
            unit="g"
        ),
        RecipeIngredient(
            recipe_id=recipes["chicken_dish"].id,
            ingredient_id=ingredients["salt"].id,
            quantity=5,
            unit="g"
        )
    ]
    db_session.add_all(recipe_ingredients)
    db_session.commit()

    return {
        "categories": categories,
        "tags": tags,
        "ingredients": ingredients,
        "recipes": recipes,
        "recipe_ingredients": recipe_ingredients
    } 