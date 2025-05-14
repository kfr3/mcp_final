# API Specification

## Base URL
```
/api/v1
```

## Endpoints

### Recipes

#### GET /recipes
List all recipes with optional filtering.

Query Parameters:
- ingredients (array): Filter by available ingredients
- dietary_restrictions (array): Filter by dietary restrictions
- search (string): Search by recipe name or description

Response:
```json
{
  "recipes": [
    {
      "id": "string",
      "name": "string",
      "description": "string",
      "preparation_time": "integer",
      "cooking_time": "integer",
      "servings": "integer",
      "ingredients": [
        {
          "id": "string",
          "name": "string",
          "quantity": "float",
          "unit": "string"
        }
      ],
      "dietary_restrictions": [
        {
          "id": "string",
          "name": "string"
        }
      ]
    }
  ],
  "total": "integer",
  "page": "integer",
  "size": "integer"
}
```

#### GET /recipes/{recipe_id}
Get a specific recipe by ID.

Response:
```json
{
  "id": "string",
  "name": "string",
  "description": "string",
  "instructions": "string",
  "preparation_time": "integer",
  "cooking_time": "integer",
  "servings": "integer",
  "ingredients": [
    {
      "id": "string",
      "name": "string",
      "quantity": "float",
      "unit": "string"
    }
  ],
  "dietary_restrictions": [
    {
      "id": "string",
      "name": "string"
    }
  ]
}
```

### Ingredients

#### GET /ingredients
List all ingredients with optional filtering.

Query Parameters:
- category (string): Filter by ingredient category
- search (string): Search by ingredient name

Response:
```json
{
  "ingredients": [
    {
      "id": "string",
      "name": "string",
      "category": {
        "id": "string",
        "name": "string"
      }
    }
  ],
  "total": "integer",
  "page": "integer",
  "size": "integer"
}
```

### Dietary Restrictions

#### GET /dietary-restrictions
List all dietary restrictions.

Response:
```json
{
  "dietary_restrictions": [
    {
      "id": "string",
      "name": "string",
      "description": "string"
    }
  ]
}
```

## Error Responses

### 400 Bad Request
```json
{
  "error": "Bad Request",
  "message": "string",
  "details": {}
}
```

### 404 Not Found
```json
{
  "error": "Not Found",
  "message": "string"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal Server Error",
  "message": "string"
}
``` 