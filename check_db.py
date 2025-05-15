from sqlalchemy import create_engine, text
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

engine = create_engine('sqlite:///recipe_bot.db')

with engine.connect() as conn:
    # Check for the ingredient 'cheese'
    cheese_query = text("SELECT * FROM ingredients WHERE name='cheese';")
    cheese_result = conn.execute(cheese_query).fetchall()
    logger.info("Cheese Ingredient: %s", cheese_result)

    # Check for the dietary tags associated with 'cheese'
    cheese_id = cheese_result[0][0] if cheese_result else None
    if cheese_id:
        dietary_tags_query = text("SELECT dt.name FROM dietary_tags dt JOIN ingredient_dietary_tags idt ON dt.id = idt.dietary_tag_id WHERE idt.ingredient_id = :cheese_id;")
        dietary_tags_result = conn.execute(dietary_tags_query, {"cheese_id": cheese_id}).fetchall()
        logger.info("Dietary Tags for Cheese: %s", dietary_tags_result)
    else:
        logger.warning("Cheese not found in the database.")

    # Check for the dietary restriction 'vegan'
    vegan_query = text("SELECT * FROM dietary_tags WHERE name='vegan';")
    vegan_result = conn.execute(vegan_query).fetchall()
    logger.info("Vegan Dietary Restriction: %s", vegan_result) 