from sqlalchemy import create_engine, text

engine = create_engine('sqlite:///recipe_bot.db')

with engine.begin() as conn:
    try:
        conn.execute(text("DROP INDEX IF EXISTS ix_ingredient_categories_id"))
        print("Index ix_ingredient_categories_id dropped.")
    except Exception as e:
        print(f"Error dropping index: {e}") 