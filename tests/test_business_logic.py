import pytest
from sqlalchemy.orm import Session
from src.business_logic import (
    RecipeMatcher,
    IngredientCompatibilityChecker,
    DietaryRestrictionValidator,
    RecipeScaler
)
from src.models import (
    Recipe,
    Ingredient,
    RecipeIngredient,
    DietaryTag,
    IngredientCategory
)

@pytest.fixture
def db_session():
    """Create a test database session"""
    from src.database.config import SessionLocal
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture
def sample_data(db_session: Session):
    """Create sample data for testing"""
    # Create categories
    vegetables = IngredientCategory(name="vegetables")
    dairy = IngredientCategory(name="dairy")
    db_session.add_all([vegetables, dairy])
    db_session.commit()

    # Create dietary tags
    vegetarian = DietaryTag(name="vegetarian")
    vegan = DietaryTag(name="vegan")
    gluten_free = DietaryTag(name="gluten-free")
    db_session.add_all([vegetarian, vegan, gluten_free])
    db_session.commit()

    # Create ingredients
    tomato = Ingredient(
        name="tomato",
        category_id=vegetables.id,
        dietary_tags=[vegetarian, vegan, gluten_free]
    )
    cheese = Ingredient(
        name="cheese",
        category_id=dairy.id,
        dietary_tags=[vegetarian, gluten_free]
    )
    db_session.add_all([tomato, cheese])
    db_session.commit()

    # Create recipe
    recipe = Recipe(
        name="Tomato and Cheese Salad",
        description="Simple salad with tomatoes and cheese",
        instructions="1. Slice tomatoes\n2. Add cheese\n3. Serve",
        preparation_time=10,
        cooking_time=0,
        difficulty="easy",
        servings=2,
        dietary_tags=[vegetarian, gluten_free]
    )
    db_session.add(recipe)
    db_session.commit()

    # Add recipe ingredients
    recipe_ingredients = [
        RecipeIngredient(
            recipe_id=recipe.id,
            ingredient_id=tomato.id,
            quantity=2,
            unit="pieces"
        ),
        RecipeIngredient(
            recipe_id=recipe.id,
            ingredient_id=cheese.id,
            quantity=100,
            unit="g"
        )
    ]
    db_session.add_all(recipe_ingredients)
    db_session.commit()

    return {
        "recipe": recipe,
        "ingredients": [tomato, cheese],
        "categories": [vegetables, dairy],
        "dietary_tags": [vegetarian, vegan, gluten_free]
    }

def test_recipe_matcher(db_session: Session, sample_data):
    """Test recipe matching functionality"""
    matcher = RecipeMatcher(db_session)
    
    # Test with matching ingredients
    matches = matcher.find_matches(
        available_ingredients=["tomato", "cheese"],
        dietary_restrictions=["vegetarian"]
    )
    assert len(matches) == 1
    assert matches[0].recipe_id == sample_data["recipe"].id
    assert matches[0].match_score == 1.0
    assert matches[0].dietary_compatibility == 1.0

    # Test with partial ingredients
    matches = matcher.find_matches(
        available_ingredients=["tomato"],
        dietary_restrictions=["vegetarian"]
    )
    assert len(matches) == 1
    assert matches[0].match_score == 0.5
    assert "cheese" in matches[0].missing_ingredients

    # Test with dietary restrictions
    matches = matcher.find_matches(
        available_ingredients=["tomato", "cheese"],
        dietary_restrictions=["vegan"]
    )
    assert len(matches) == 0  # No matches because cheese is not vegan

    # Test with no dietary restrictions
    matches = matcher.find_matches(
        available_ingredients=["tomato", "cheese"],
        dietary_restrictions=[]
    )
    assert len(matches) == 1
    assert matches[0].recipe_id == sample_data["recipe"].id
    assert matches[0].dietary_compatibility == 1.0

def test_ingredient_compatibility(db_session: Session, sample_data):
    """Test ingredient compatibility checking"""
    checker = IngredientCompatibilityChecker(db_session)
    
    # Test compatible ingredients
    score, reasons = checker.check_compatibility("tomato", "cheese")
    assert score > 0
    assert "Common dietary tags" in reasons[0]

    # Test incompatible ingredients
    score, reasons = checker.check_compatibility("tomato", "invalid_ingredient")
    assert score == 0
    assert "not found" in reasons[0]

def test_dietary_restriction_validator(db_session: Session, sample_data):
    """Test dietary restriction validation"""
    validator = DietaryRestrictionValidator(db_session)
    
    # Test valid recipe
    is_valid, messages = validator.validate_recipe(
        sample_data["recipe"].id,
        ["vegetarian", "gluten-free"]
    )
    assert is_valid
    assert "meets all dietary restrictions" in messages[0]

    # Test invalid recipe
    is_valid, messages = validator.validate_recipe(
        sample_data["recipe"].id,
        ["vegan"]
    )
    assert not is_valid
    assert "Missing dietary restrictions" in messages[0]

    # Test ingredient validation
    is_valid, messages = validator.validate_ingredients(
        ["tomato", "cheese"],
        ["vegetarian"]
    )
    assert is_valid
    assert len(messages) == 0

def test_recipe_scaler(db_session: Session, sample_data):
    """Test recipe scaling functionality"""
    scaler = RecipeScaler(db_session)
    
    # Test scaling up
    scaled_recipe = scaler.scale_recipe(
        sample_data["recipe"].id,
        target_servings=4
    )
    assert scaled_recipe["target_servings"] == 4
    assert scaled_recipe["scaling_factor"] == 2.0
    assert len(scaled_recipe["ingredients"]) == 2
    assert scaled_recipe["ingredients"][0]["quantity"] == 4  # 2 tomatoes * 2
    assert scaled_recipe["ingredients"][1]["quantity"] == 200  # 100g cheese * 2

    # Test scaling down
    scaled_recipe = scaler.scale_recipe(
        sample_data["recipe"].id,
        target_servings=1
    )
    assert scaled_recipe["target_servings"] == 1
    assert scaled_recipe["scaling_factor"] == 0.5
    assert scaled_recipe["ingredients"][0]["quantity"] == 1  # 2 tomatoes * 0.5
    assert scaled_recipe["ingredients"][1]["quantity"] == 50  # 100g cheese * 0.5 