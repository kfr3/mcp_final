# MCP Tools Design

## Overview
MCP tools provide functionality for recipe-related operations. Each tool is designed to handle specific tasks and follows a consistent input/output format.

## Tool Specifications

### 1. find_recipes
Finds recipes based on available ingredients and dietary restrictions.

#### Input Parameters
```json
{
  "ingredients": [
    {
      "id": "string",
      "quantity": "float",
      "unit": "string"
    }
  ],
  "dietary_restrictions": ["string"],
  "max_missing_ingredients": "integer",
  "preferred_categories": ["string"]
}
```

#### Output Format
```json
{
  "recipes": [
    {
      "id": "string",
      "name": "string",
      "match_percentage": "float",
      "missing_ingredients": [
        {
          "id": "string",
          "name": "string",
          "quantity": "float",
          "unit": "string"
        }
      ],
      "preparation_time": "integer",
      "cooking_time": "integer",
      "difficulty": "string"
    }
  ],
  "total_matches": "integer"
}
```

### 2. suggest_substitutions
Suggests ingredient substitutions based on dietary restrictions and availability.

#### Input Parameters
```json
{
  "ingredient_id": "string",
  "dietary_restrictions": ["string"],
  "available_ingredients": ["string"],
  "quantity": "float",
  "unit": "string"
}
```

#### Output Format
```json
{
  "substitutions": [
    {
      "ingredient_id": "string",
      "name": "string",
      "quantity": "float",
      "unit": "string",
      "match_score": "float",
      "notes": "string"
    }
  ],
  "original_ingredient": {
    "id": "string",
    "name": "string",
    "category": "string"
  }
}
```

### 3. analyze_ingredients
Analyzes a list of ingredients for nutritional information and dietary compatibility.

#### Input Parameters
```json
{
  "ingredients": [
    {
      "id": "string",
      "quantity": "float",
      "unit": "string"
    }
  ],
  "dietary_restrictions": ["string"]
}
```

#### Output Format
```json
{
  "analysis": {
    "total_calories": "float",
    "macronutrients": {
      "protein": "float",
      "carbohydrates": "float",
      "fat": "float"
    },
    "dietary_compatibility": {
      "compatible": ["string"],
      "incompatible": ["string"]
    },
    "missing_nutrients": ["string"],
    "suggestions": ["string"]
  }
}
```

### 4. scale_recipe
Scales a recipe's ingredients and cooking times based on desired servings.

#### Input Parameters
```json
{
  "recipe_id": "string",
  "target_servings": "integer",
  "adjust_cooking_time": "boolean"
}
```

#### Output Format
```json
{
  "scaled_recipe": {
    "id": "string",
    "name": "string",
    "original_servings": "integer",
    "new_servings": "integer",
    "ingredients": [
      {
        "id": "string",
        "name": "string",
        "original_quantity": "float",
        "new_quantity": "float",
        "unit": "string"
      }
    ],
    "cooking_time": {
      "original": "integer",
      "adjusted": "integer"
    }
  }
}
```

## Error Handling

### Invalid Input
```json
{
  "error": "InvalidInput",
  "message": "The provided input parameters are invalid",
  "details": {
    "field": "string",
    "reason": "string"
  }
}
```

### Resource Not Found
```json
{
  "error": "ResourceNotFound",
  "message": "The requested resource was not found",
  "resource": "string",
  "identifier": "string"
}
```

### Processing Error
```json
{
  "error": "ProcessingError",
  "message": "An error occurred while processing the request",
  "details": "string"
}
```

## Usage Examples

### Find Recipes with Available Ingredients
```json
{
  "ingredients": [
    {"id": "1", "quantity": 2, "unit": "cups"},
    {"id": "2", "quantity": 1, "unit": "tbsp"}
  ],
  "dietary_restrictions": ["vegetarian"],
  "max_missing_ingredients": 2
}
```

### Suggest Substitutions for an Ingredient
```json
{
  "ingredient_id": "3",
  "dietary_restrictions": ["vegan"],
  "available_ingredients": ["4", "5", "6"],
  "quantity": 1,
  "unit": "cup"
}
```

### Analyze a List of Ingredients
```json
{
  "ingredients": [
    {"id": "1", "quantity": 100, "unit": "g"},
    {"id": "2", "quantity": 2, "unit": "tbsp"}
  ],
  "dietary_restrictions": ["gluten-free"]
}
```

### Scale a Recipe
```json
{
  "recipe_id": "123",
  "target_servings": 8,
  "adjust_cooking_time": true
}
``` 