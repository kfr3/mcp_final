from sqlalchemy import create_engine, text

# Connect to the database in the project root
engine = create_engine('sqlite:///recipe_bot.db')

delete_sql = '''
DELETE FROM ingredients
WHERE rowid NOT IN (
    SELECT MIN(rowid)
    FROM ingredients
    GROUP BY name
);
'''

with engine.begin() as conn:
    result = conn.execute(text(delete_sql))
    print(f"Removed {result.rowcount} duplicate ingredient(s).")

# Optionally, re-run the duplicate check
duplicate_check_sql = "SELECT name, COUNT(*) as count FROM ingredients GROUP BY name HAVING count > 1"
with engine.connect() as conn:
    duplicates = conn.execute(text(duplicate_check_sql)).fetchall()
    if duplicates:
        print("Duplicates still present:")
        for name, count in duplicates:
            print(f"{name}: {count} times")
    else:
        print("No duplicate ingredient names remain.") 