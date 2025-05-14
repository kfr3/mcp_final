# Prompt Engineering

## Overview
This document outlines the optimized prompts for different recipe-related tasks. Each prompt is designed to work effectively with LLMs while maintaining consistency and accuracy.

## Recipe Generation

### Base Prompt
```
You are a professional chef and recipe creator. Create a recipe that meets the following criteria:
- Cuisine type: {cuisine_type}
- Dietary restrictions: {dietary_restrictions}
- Available ingredients: {ingredients}
- Cooking skill level: {skill_level}
- Servings: {servings}

The recipe should include:
1. A descriptive name
2. A brief introduction
3. List of ingredients with precise measurements
4. Step-by-step instructions
5. Cooking time and preparation time
6. Difficulty level
7. Any special notes or tips
```

### Example
```
You are a professional chef and recipe creator. Create a recipe that meets the following criteria:
- Cuisine type: Italian
- Dietary restrictions: vegetarian, gluten-free
- Available ingredients: tomatoes, basil, mozzarella, olive oil, garlic
- Cooking skill level: intermediate
- Servings: 4

The recipe should include:
1. A descriptive name
2. A brief introduction
3. List of ingredients with precise measurements
4. Step-by-step instructions
5. Cooking time and preparation time
6. Difficulty level
7. Any special notes or tips
```

## Ingredient Analysis

### Base Prompt
```
Analyze the following ingredients for a recipe:
{ingredients_list}

Consider:
1. Nutritional value
2. Dietary compatibility with: {dietary_restrictions}
3. Potential substitutions
4. Storage recommendations
5. Seasonal availability

Provide a detailed analysis in the following format:
- Nutritional breakdown
- Dietary compatibility assessment
- Substitution suggestions
- Storage and handling tips
- Seasonal considerations
```

### Example
```
Analyze the following ingredients for a recipe:
- 2 cups all-purpose flour
- 3 eggs
- 1 cup milk
- 2 tbsp butter

Consider:
1. Nutritional value
2. Dietary compatibility with: vegan, gluten-free
3. Potential substitutions
4. Storage recommendations
5. Seasonal availability

Provide a detailed analysis in the following format:
- Nutritional breakdown
- Dietary compatibility assessment
- Substitution suggestions
- Storage and handling tips
- Seasonal considerations
```

## Dietary Restriction Handling

### Base Prompt
```
Review the following recipe for dietary restrictions:
{recipe_details}

Dietary restrictions to consider:
{dietary_restrictions}

Provide:
1. Compatibility assessment
2. Required modifications
3. Alternative ingredients
4. Cross-contamination risks
5. Safe preparation methods

Format the response as:
- Compatibility summary
- Required changes
- Ingredient alternatives
- Safety considerations
- Preparation guidelines
```

### Example
```
Review the following recipe for dietary restrictions:
Recipe: Classic Chocolate Cake
Ingredients: flour, sugar, eggs, milk, butter, cocoa powder

Dietary restrictions to consider:
- Gluten-free
- Dairy-free
- Nut-free

Provide:
1. Compatibility assessment
2. Required modifications
3. Alternative ingredients
4. Cross-contamination risks
5. Safe preparation methods

Format the response as:
- Compatibility summary
- Required changes
- Ingredient alternatives
- Safety considerations
- Preparation guidelines
```

## Cooking Instructions

### Base Prompt
```
Provide detailed cooking instructions for the following recipe:
{recipe_name}

Consider:
1. Skill level: {skill_level}
2. Available equipment: {equipment}
3. Time constraints: {time_constraints}
4. Special requirements: {special_requirements}

Structure the instructions as:
1. Preparation steps
2. Cooking process
3. Timing guidelines
4. Temperature control
5. Safety precautions
6. Serving suggestions
```

### Example
```
Provide detailed cooking instructions for the following recipe:
Recipe: Homemade Pizza

Consider:
1. Skill level: beginner
2. Available equipment: basic kitchen tools, oven
3. Time constraints: 1 hour total
4. Special requirements: none

Structure the instructions as:
1. Preparation steps
2. Cooking process
3. Timing guidelines
4. Temperature control
5. Safety precautions
6. Serving suggestions
```

## Best Practices

### 1. Clarity and Specificity
- Use clear, unambiguous language
- Include specific measurements and units
- Define any technical terms
- Provide context when needed

### 2. Structure and Format
- Use consistent formatting
- Break down complex tasks
- Include step numbers
- Use bullet points for lists

### 3. Safety and Dietary Considerations
- Always include safety warnings
- Highlight dietary restrictions
- Mention potential allergens
- Include storage guidelines

### 4. Adaptability
- Allow for ingredient substitutions
- Consider different skill levels
- Account for equipment variations
- Include timing flexibility

### 5. User Experience
- Keep instructions concise
- Use active voice
- Include helpful tips
- Provide visual cues when possible 