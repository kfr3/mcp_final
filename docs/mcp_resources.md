# MCP Resources Design

## Overview
MCP (Model Context Protocol) resources provide a standardized way to access and manipulate recipe-related data. Each resource follows the `resource://{identifier}` format and returns structured data.

## Resource Endpoints

### 1. Ingredients Resource
```
ingredients://{category}
```

#### Purpose
Retrieves ingredients filtered by category.

#### Parameters
- `category` (string): The category identifier to filter ingredients by

#### Response Format
```json
{
  "ingredients": [
    {
      "id": "string",
      "name": "string",
      "category": {
        "id": "string",
        "name": "string",
        "description": "string"
      },
      "dietary_tags": [
        {
          "id": "string",
          "name": "string",
          "description": "string"
        }
      ]
    }
  ]
}
```

### 2. Recipe Resource
```
recipe://{recipe_id}
```

#### Purpose
Retrieves detailed information about a specific recipe.

#### Parameters
- `recipe_id` (string): The unique identifier of the recipe

#### Response Format
```json
{
  "id": "string",
  "name": "string",
  "description": "string",
  "instructions": "string",
  "preparation_time": "integer",
  "cooking_time": "integer",
  "difficulty": "string",
  "servings": "integer",
  "ingredients": [
    {
      "id": "string",
      "name": "string",
      "quantity": "float",
      "unit": "string",
      "category": {
        "id": "string",
        "name": "string"
      }
    }
  ],
  "dietary_tags": [
    {
      "id": "string",
      "name": "string",
      "description": "string"
    }
  ]
}
```

### 3. Categories Resource
```
categories://all
```

#### Purpose
Retrieves all available ingredient categories.

#### Response Format
```json
{
  "categories": [
    {
      "id": "string",
      "name": "string",
      "description": "string",
      "ingredient_count": "integer"
    }
  ]
}
```

### 4. Dietary Restrictions Resource
```
dietary://restrictions
```

#### Purpose
Retrieves all available dietary restrictions and preferences.

#### Response Format
```json
{
  "dietary_restrictions": [
    {
      "id": "string",
      "name": "string",
      "description": "string",
      "recipe_count": "integer",
      "ingredient_count": "integer"
    }
  ]
}
```

## Error Handling

### Resource Not Found
```json
{
  "error": "ResourceNotFound",
  "message": "The requested resource was not found",
  "resource": "string",
  "identifier": "string"
}
```

### Invalid Category
```json
{
  "error": "InvalidCategory",
  "message": "The specified category is not valid",
  "category": "string",
  "available_categories": ["string"]
}
```

### Invalid Recipe ID
```json
{
  "error": "InvalidRecipeId",
  "message": "The specified recipe ID is not valid",
  "recipe_id": "string"
}
```

## Usage Examples

### Get All Vegetables
```
ingredients://vegetables
```

### Get Specific Recipe
```
recipe://123
```

### Get All Categories
```
categories://all
```

### Get All Dietary Restrictions
```
dietary://restrictions
``` 