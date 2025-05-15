from sqlalchemy import inspect
from database.config import engine

def test_database_connection():
    # Create an inspector
    inspector = inspect(engine)
    
    # Get all table names
    table_names = inspector.get_table_names()
    
    print("Successfully connected to the database!")
    print("\nCreated tables:")
    for table in table_names:
        print(f"- {table}")
        
        # Get columns for each table
        columns = inspector.get_columns(table)
        print("  Columns:")
        for column in columns:
            print(f"    - {column['name']}: {column['type']}")

if __name__ == "__main__":
    test_database_connection() 