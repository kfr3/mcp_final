from typing import List, Dict, Any, Optional
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError as PydanticValidationError
import logging
from datetime import datetime
import traceback
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('recipe_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Custom Exceptions
class RecipeBotError(Exception):
    """Base exception for Recipe Bot errors"""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class RecipeValidationError(RecipeBotError):
    """Raised when input validation fails"""
    def __init__(self, message: str):
        super().__init__(message, status_code=400)

class ResourceNotFoundError(RecipeBotError):
    """Raised when a requested resource is not found"""
    def __init__(self, resource_type: str, resource_id: str):
        message = f"{resource_type} with id {resource_id} not found"
        super().__init__(message, status_code=404)

class DatabaseError(RecipeBotError):
    """Raised when a database operation fails"""
    def __init__(self, message: str):
        super().__init__(message, status_code=500)

# Input Validation Models
class RecipeInput(BaseModel):
    name: str
    description: str
    instructions: str
    preparation_time: int
    cooking_time: int
    difficulty: str
    servings: int
    ingredients: List[Dict[str, Any]]
    dietary_tags: List[str]

    class Config:
        schema_extra = {
            "example": {
                "name": "Spaghetti Carbonara",
                "description": "Classic Italian pasta dish",
                "instructions": "1. Cook pasta\n2. Mix eggs and cheese\n3. Combine with hot pasta",
                "preparation_time": 15,
                "cooking_time": 20,
                "difficulty": "medium",
                "servings": 4,
                "ingredients": [
                    {"name": "spaghetti", "quantity": 500, "unit": "g"},
                    {"name": "eggs", "quantity": 4, "unit": "pieces"}
                ],
                "dietary_tags": ["vegetarian"]
            }
        }

class IngredientInput(BaseModel):
    name: str
    category: str
    dietary_tags: List[str]

    class Config:
        schema_extra = {
            "example": {
                "name": "olive oil",
                "category": "oils",
                "dietary_tags": ["vegan", "vegetarian", "gluten-free"]
            }
        }

# Error Handling Middleware
async def error_handler(request: Request, exc: Exception) -> JSONResponse:
    """Global error handler for the application"""
    if isinstance(exc, RecipeBotError):
        status_code = exc.status_code
        error_message = exc.message
    elif isinstance(exc, RecipeValidationError):
        status_code = 400
        error_message = str(exc)
    else:
        status_code = 500
        error_message = "Internal server error"

    # Log the error
    logger.error(
        f"Error occurred: {error_message}\n"
        f"Path: {request.url.path}\n"
        f"Method: {request.method}\n"
        f"Traceback: {traceback.format_exc()}"
    )

    return JSONResponse(
        status_code=status_code,
        content={
            "error": error_message,
            "timestamp": datetime.utcnow().isoformat(),
            "path": request.url.path
        }
    )

# Input Validation Functions
def validate_recipe_input(data: Dict[str, Any]) -> RecipeInput:
    """Validate recipe input data"""
    try:
        return RecipeInput(**data)
    except PydanticValidationError as e:
        raise RecipeValidationError(f"Invalid recipe data: {str(e)}")

def validate_ingredient_input(data: Dict[str, Any]) -> IngredientInput:
    """Validate ingredient input data"""
    try:
        return IngredientInput(**data)
    except PydanticValidationError as e:
        raise RecipeValidationError(f"Invalid ingredient data: {str(e)}")

# Error Recovery Mechanisms
class ErrorRecovery:
    @staticmethod
    def retry_operation(operation, max_retries: int = 3, delay: float = 1.0):
        """Retry an operation with exponential backoff"""
        import time
        for attempt in range(max_retries):
            try:
                return operation()
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                logger.warning(f"Operation failed, retrying... (attempt {attempt + 1}/{max_retries})")
                time.sleep(delay * (2 ** attempt))

    @staticmethod
    def handle_database_error(error: Exception) -> Dict[str, Any]:
        """Handle database errors and provide recovery information"""
        error_info = {
            "error_type": type(error).__name__,
            "message": str(error),
            "timestamp": datetime.utcnow().isoformat(),
            "recovery_suggestions": []
        }

        if "connection" in str(error).lower():
            error_info["recovery_suggestions"].append(
                "Check database connection settings and network connectivity"
            )
        elif "constraint" in str(error).lower():
            error_info["recovery_suggestions"].append(
                "Verify that the data meets all database constraints"
            )
        elif "timeout" in str(error).lower():
            error_info["recovery_suggestions"].append(
                "Consider increasing database timeout settings"
            )

        return error_info

# Request Validation Middleware
async def validate_request(request: Request) -> None:
    """Validate incoming request data"""
    try:
        if request.method in ["POST", "PUT"]:
            body = await request.json()
            if "recipe" in request.url.path:
                validate_recipe_input(body)
            elif "ingredient" in request.url.path:
                validate_ingredient_input(body)
    except json.JSONDecodeError:
        raise RecipeValidationError("Invalid JSON data in request body")
    except Exception as e:
        raise RecipeValidationError(f"Request validation failed: {str(e)}")

# Error Logging
def log_error(error: Exception, context: Dict[str, Any] = None) -> None:
    """Log error with context information"""
    error_data = {
        "error_type": type(error).__name__,
        "message": str(error),
        "timestamp": datetime.utcnow().isoformat(),
        "traceback": traceback.format_exc()
    }
    if context:
        error_data["context"] = context

    logger.error(json.dumps(error_data, indent=2)) 