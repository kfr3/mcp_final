import pytest
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from src.models import (
    Recipe,
    Ingredient,
    RecipeIngredient,
    DietaryTag,
    IngredientCategory
)

def test_recipe_model(db_session: Session):
    """Test Recipe model creation and relationships"""
    # Create test data
    category = IngredientCategory(name="vegetables_recipe_test")
    db_session.add(category)
    db_session.commit()

    tag = DietaryTag(name="vegetarian_recipe_test")
    db_session.add(tag)
    db_session.commit()

    ingredient = Ingredient(
        name="tomato_recipe_test",
        category_id=category.id,
        dietary_tags=[tag]
    )
    db_session.add(ingredient)
    db_session.commit()

    # Create recipe
    recipe = Recipe(
        name="Test Recipe",
        description="Test Description",
        instructions="Test Instructions",
        preparation_time=30,
        cooking_time=60,
        difficulty="easy",
        servings=4,
        dietary_tags=[tag]
    )
    db_session.add(recipe)
    db_session.commit()

    # Add recipe ingredient
    recipe_ingredient = RecipeIngredient(
        recipe_id=recipe.id,
        ingredient_id=ingredient.id,
        quantity=2,
        unit="pieces"
    )
    db_session.add(recipe_ingredient)
    db_session.commit()

    # Test recipe attributes
    assert recipe.name == "Test Recipe"
    assert recipe.description == "Test Description"
    assert recipe.instructions == "Test Instructions"
    assert recipe.preparation_time == 30
    assert recipe.cooking_time == 60
    assert recipe.difficulty == "easy"
    assert recipe.servings == 4
    assert len(recipe.dietary_tags) == 1
    assert recipe.dietary_tags[0].name == "vegetarian_recipe_test"
    assert len(recipe.ingredients) == 1
    assert recipe.ingredients[0].ingredient.name == "tomato_recipe_test"

def test_ingredient_model(db_session: Session):
    """Test Ingredient model creation and relationships"""
    # Create test data
    category = IngredientCategory(name="vegetables_ingredient_test")
    db_session.add(category)
    db_session.commit()

    tag = DietaryTag(name="vegetarian_ingredient_test")
    db_session.add(tag)
    db_session.commit()

    # Create ingredient
    ingredient = Ingredient(
        name="tomato_ingredient_test",
        category_id=category.id,
        dietary_tags=[tag]
    )
    db_session.add(ingredient)
    db_session.commit()

    # Test ingredient attributes
    assert ingredient.name == "tomato_ingredient_test"
    assert ingredient.category.name == "vegetables_ingredient_test"
    assert len(ingredient.dietary_tags) == 1
    assert ingredient.dietary_tags[0].name == "vegetarian_ingredient_test"

def test_recipe_ingredient_model(db_session: Session):
    """Test RecipeIngredient model creation and relationships"""
    # Create test data
    category = IngredientCategory(name="vegetables_recipe_ingredient_test")
    db_session.add(category)
    db_session.commit()

    ingredient = Ingredient(
        name="tomato_recipe_ingredient_test",
        category_id=category.id
    )
    db_session.add(ingredient)
    db_session.commit()

    recipe = Recipe(
        name="Test Recipe RI",
        description="Test Description",
        instructions="Test Instructions",
        preparation_time=30,
        cooking_time=60,
        difficulty="easy",
        servings=4
    )
    db_session.add(recipe)
    db_session.commit()

    # Create recipe ingredient
    recipe_ingredient = RecipeIngredient(
        recipe_id=recipe.id,
        ingredient_id=ingredient.id,
        quantity=2,
        unit="pieces"
    )
    db_session.add(recipe_ingredient)
    db_session.commit()

    # Test recipe ingredient attributes
    assert recipe_ingredient.recipe.name == "Test Recipe RI"
    assert recipe_ingredient.ingredient.name == "tomato_recipe_ingredient_test"
    assert recipe_ingredient.quantity == 2
    assert recipe_ingredient.unit == "pieces"

def test_dietary_tag_model(db_session: Session):
    """Test DietaryTag model creation and relationships"""
    # Create test data
    tag = DietaryTag(name="vegetarian_tag_test")
    db_session.add(tag)
    db_session.commit()

    # Create recipe with tag
    recipe = Recipe(
        name="Test Recipe Tag",
        description="Test Description",
        instructions="Test Instructions",
        preparation_time=30,
        cooking_time=60,
        difficulty="easy",
        servings=4,
        dietary_tags=[tag]
    )
    db_session.add(recipe)
    db_session.commit()

    # Test tag attributes and relationships
    assert tag.name == "vegetarian_tag_test"
    assert len(tag.recipes) == 1
    assert tag.recipes[0].name == "Test Recipe Tag"

def test_ingredient_category_model(db_session: Session):
    """Test IngredientCategory model creation and relationships"""
    # Create test data
    category = IngredientCategory(name="vegetables_category_test")
    db_session.add(category)
    db_session.commit()

    # Create ingredient in category
    ingredient = Ingredient(
        name="tomato_category_test",
        category_id=category.id
    )
    db_session.add(ingredient)
    db_session.commit()

    # Test category attributes and relationships
    assert category.name == "vegetables_category_test"
    assert len(category.ingredients) == 1
    assert category.ingredients[0].name == "tomato_category_test"

def test_model_constraints(db_session: Session):
    """Test model constraints and validations"""
    # Test unique ingredient name
    category = IngredientCategory(name="vegetables_constraints_test")
    db_session.add(category)
    db_session.commit()

    ingredient1 = Ingredient(name="tomato_constraints_test", category_id=category.id)
    db_session.add(ingredient1)
    db_session.commit()

    ingredient2 = Ingredient(name="tomato_constraints_test", category_id=category.id)
    db_session.add(ingredient2)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()

    # Test unique category name
    category1 = IngredientCategory(name="vegetables_constraints_test2")
    db_session.add(category1)
    db_session.commit()

    category2 = IngredientCategory(name="vegetables_constraints_test2")
    db_session.add(category2)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()

    # Test unique dietary tag name
    tag1 = DietaryTag(name="vegetarian_constraints_test")
    db_session.add(tag1)
    db_session.commit()

    tag2 = DietaryTag(name="vegetarian_constraints_test")
    db_session.add(tag2)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback() 