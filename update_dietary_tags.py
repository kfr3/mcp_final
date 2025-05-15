from sqlalchemy import create_engine, text

engine = create_engine('sqlite:///recipe_bot.db')

with engine.begin() as conn:
    # Get the ID of the 'cheese' ingredient
    cheese_query = text("SELECT id FROM ingredients WHERE name='cheese';")
    cheese_id = conn.execute(cheese_query).scalar()

    # Get the ID of the 'vegan' dietary tag
    vegan_query = text("SELECT id FROM dietary_tags WHERE name='vegan';")
    vegan_id = conn.execute(vegan_query).scalar()

    if cheese_id and vegan_id:
        # Insert the association between 'cheese' and 'vegan'
        insert_query = text("INSERT INTO ingredient_dietary_tags (ingredient_id, dietary_tag_id) VALUES (:cheese_id, :vegan_id);")
        conn.execute(insert_query, {"cheese_id": cheese_id, "vegan_id": vegan_id})
        print("Updated dietary tags for 'cheese' to include 'vegan'.")
    else:
        print("Ingredient 'cheese' or dietary tag 'vegan' not found in the database.") 