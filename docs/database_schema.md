# Database Schema Design

## Tables

### Recipes
- id (Primary Key)
- name (String)
- description (Text)
- instructions (Text)
- preparation_time (Integer, minutes)
- cooking_time (Integer, minutes)
- servings (Integer)
- created_at (DateTime)
- updated_at (DateTime)

### Ingredients
- id (Primary Key)
- name (String)
- category_id (Foreign Key -> IngredientCategories)
- created_at (DateTime)
- updated_at (DateTime)

### IngredientCategories
- id (Primary Key)
- name (String)
- description (Text)
- created_at (DateTime)
- updated_at (DateTime)

### DietaryRestrictions
- id (Primary Key)
- name (String)
- description (Text)
- created_at (DateTime)
- updated_at (DateTime)

### RecipeIngredients
- id (Primary Key)
- recipe_id (Foreign Key -> Recipes)
- ingredient_id (Foreign Key -> Ingredients)
- quantity (Float)
- unit (String)
- created_at (DateTime)
- updated_at (DateTime)

### RecipeDietaryRestrictions
- id (Primary Key)
- recipe_id (Foreign Key -> Recipes)
- dietary_restriction_id (Foreign Key -> DietaryRestrictions)
- created_at (DateTime)
- updated_at (DateTime)

## Relationships
- A Recipe can have multiple Ingredients (Many-to-Many through RecipeIngredients)
- An Ingredient belongs to one Category (Many-to-One)
- A Recipe can have multiple Dietary Restrictions (Many-to-Many through RecipeDietaryRestrictions)
- An Ingredient can be used in multiple Recipes (Many-to-Many through RecipeIngredients)
- A Dietary Restriction can apply to multiple Recipes (Many-to-Many through RecipeDietaryRestrictions) 