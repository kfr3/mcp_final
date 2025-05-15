from sqlalchemy import create_engine, text

# Adjusted path to point to the project root
engine = create_engine('sqlite:///recipe_bot.db')

with engine.connect() as conn:
    result = conn.execute(
        text("SELECT name, COUNT(*) as count FROM ingredients GROUP BY name HAVING count > 1")
    )
    duplicates = result.fetchall()
    if duplicates:
        print("Duplicate ingredient names found:")
        for name, count in duplicates:
            print(f"{name}: {count} times")
    else:
        print("No duplicate ingredient names found.") 