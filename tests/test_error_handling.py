import pytest
from fastapi import Request
from pydantic import ValidationError as PydanticValidationError
from src.error_handling import (
    RecipeBotError,
    RecipeValidationError,
    ResourceNotFoundError,
    DatabaseError,
    RecipeInput,
    IngredientInput,
    error_handler,
    validate_recipe_input,
    validate_ingredient_input,
    ErrorRecovery,
    validate_request,
    log_error
)
import json
from datetime import datetime

@pytest.fixture
def mock_request():
    """Create a mock FastAPI request"""
    class MockRequest:
        def __init__(self, method="GET", path="/test", body=None):
            self.method = method
            self.url = type("URL", (), {"path": path})
            self._body = body

        async def json(self):
            return self._body

    return MockRequest

def test_custom_exceptions():
    """Test custom exception classes"""
    # Test base exception
    error = RecipeBotError("Test error", 400)
    assert error.message == "Test error"
    assert error.status_code == 400

    # Test validation error
    error = RecipeValidationError("Invalid input")
    assert error.message == "Invalid input"
    assert error.status_code == 400

    # Test resource not found error
    error = ResourceNotFoundError("recipe", "123")
    assert "recipe with id 123 not found" in error.message
    assert error.status_code == 404

    # Test database error
    error = DatabaseError("Connection failed")
    assert error.message == "Connection failed"
    assert error.status_code == 500

def test_validation_models():
    """Test input validation models"""
    # Test valid recipe input
    valid_recipe = {
        "name": "Test Recipe",
        "description": "Test Description",
        "instructions": "Test Instructions",
        "preparation_time": 30,
        "cooking_time": 60,
        "difficulty": "easy",
        "servings": 4,
        "ingredients": [],
        "dietary_tags": []
    }
    recipe = RecipeInput.model_validate(valid_recipe)
    assert isinstance(recipe, RecipeInput)
    assert recipe.name == "Test Recipe"
    
    # Test invalid recipe input
    invalid_recipe = valid_recipe.copy()
    invalid_recipe["preparation_time"] = "invalid"  # Should be int
    with pytest.raises(PydanticValidationError):
        RecipeInput.model_validate(invalid_recipe)

    # Test valid ingredient input
    valid_ingredient = {
        "name": "Test Ingredient",
        "category": "vegetables",
        "dietary_tags": ["vegetarian"]
    }
    ingredient = IngredientInput.model_validate(valid_ingredient)
    assert isinstance(ingredient, IngredientInput)
    assert ingredient.name == "Test Ingredient"

    # Test invalid ingredient input
    invalid_ingredient = valid_ingredient.copy()
    invalid_ingredient["name"] = ""  # Empty name should be invalid
    with pytest.raises(PydanticValidationError):
        IngredientInput.model_validate(invalid_ingredient)

@pytest.mark.asyncio
async def test_error_handler():
    """Test the error handler middleware"""
    # Create a mock request
    request = Request({
        "type": "http",
        "method": "GET",
        "path": "/test",
        "headers": {},
        "query_params": {},
        "client": None,
        "app": None,
        "state": {},
        "scope": {"type": "http", "method": "GET", "path": "/test"}
    })
    
    # Test RecipeBotError
    error = RecipeBotError("Test error", 400)
    response = await error_handler(request, error)
    assert response.status_code == 400
    assert "Test error" in response.body.decode()
    
    # Test RecipeValidationError
    error = RecipeValidationError("Validation error")
    response = await error_handler(request, error)
    assert response.status_code == 400
    assert "Validation error" in response.body.decode()
    
    # Test unknown error
    error = Exception("Unknown error")
    response = await error_handler(request, error)
    assert response.status_code == 500
    assert "Internal server error" in response.body.decode()

def test_error_recovery():
    """Test error recovery mechanisms"""
    # Test retry operation
    attempts = 0
    def failing_operation():
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise Exception("Temporary failure")
        return "success"

    result = ErrorRecovery.retry_operation(failing_operation, max_retries=3)
    assert result == "success"
    assert attempts == 3

    # Test database error handling
    error = Exception("Database connection failed")
    error_info = ErrorRecovery.handle_database_error(error)
    assert "connection" in error_info["recovery_suggestions"][0].lower()
    assert "error_type" in error_info
    assert "timestamp" in error_info

@pytest.mark.asyncio
async def test_request_validation():
    """Test request validation middleware"""
    # Create a mock request with valid data
    valid_data = {
        "name": "Test Recipe",
        "description": "Test",
        "instructions": "Test",
        "preparation_time": 30,
        "cooking_time": 60,
        "difficulty": "medium",
        "servings": 4,
        "ingredients": [],
        "dietary_tags": []
    }
    
    class MockRequest:
        def __init__(self, method, path, body):
            self.method = method
            self.url = type("URL", (), {"path": path})
            self._body = body
            self._json = body

        async def json(self):
            return self._json

    # Test valid request
    valid_request = MockRequest("POST", "/recipe", valid_data)
    await validate_request(valid_request)  # Should not raise
    
    # Test invalid request
    invalid_data = valid_data.copy()
    invalid_data["preparation_time"] = "30"  # Should be int
    invalid_request = MockRequest("POST", "/recipe", invalid_data)
    
    with pytest.raises(RecipeValidationError) as exc_info:
        await validate_request(invalid_request)
    assert "preparation_time" in str(exc_info.value)

def test_error_logging(caplog):
    """Test error logging functionality"""
    error = Exception("Test error")
    context = {"user_id": "123", "action": "test"}
    
    log_error(error, context)
    
    assert "Test error" in caplog.text
    assert "user_id" in caplog.text
    assert "action" in caplog.text
    assert "timestamp" in caplog.text 