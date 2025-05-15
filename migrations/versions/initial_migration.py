"""initial migration

Revision ID: 001
Revises: 
Create Date: 2024-03-19 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create ingredient_categories table
    op.create_table(
        'ingredient_categories',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )

    # Create dietary_tags table
    op.create_table(
        'dietary_tags',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )

    # Create recipes table
    op.create_table(
        'recipes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('instructions', sa.Text(), nullable=False),
        sa.Column('preparation_time', sa.Integer(), nullable=False),
        sa.Column('cooking_time', sa.Integer(), nullable=False),
        sa.Column('difficulty', sa.String(length=50), nullable=False),
        sa.Column('servings', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_recipes_name'), 'recipes', ['name'], unique=False)

    # Create ingredients table
    op.create_table(
        'ingredients',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('category_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['category_id'], ['ingredient_categories.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ingredients_name'), 'ingredients', ['name'], unique=False)

    # Create recipe_ingredients table
    op.create_table(
        'recipe_ingredients',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('recipe_id', sa.Integer(), nullable=False),
        sa.Column('ingredient_id', sa.Integer(), nullable=False),
        sa.Column('quantity', sa.Float(), nullable=False),
        sa.Column('unit', sa.String(length=50), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['ingredient_id'], ['ingredients.id'], ),
        sa.ForeignKeyConstraint(['recipe_id'], ['recipes.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create recipe_dietary_tags association table
    op.create_table(
        'recipe_dietary_tags',
        sa.Column('recipe_id', sa.Integer(), nullable=False),
        sa.Column('dietary_tag_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['dietary_tag_id'], ['dietary_tags.id'], ),
        sa.ForeignKeyConstraint(['recipe_id'], ['recipes.id'], ),
        sa.PrimaryKeyConstraint('recipe_id', 'dietary_tag_id')
    )

    # Create ingredient_dietary_tags association table
    op.create_table(
        'ingredient_dietary_tags',
        sa.Column('ingredient_id', sa.Integer(), nullable=False),
        sa.Column('dietary_tag_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['dietary_tag_id'], ['dietary_tags.id'], ),
        sa.ForeignKeyConstraint(['ingredient_id'], ['ingredients.id'], ),
        sa.PrimaryKeyConstraint('ingredient_id', 'dietary_tag_id')
    )

def downgrade():
    # Drop all tables in reverse order
    op.drop_table('ingredient_dietary_tags')
    op.drop_table('recipe_dietary_tags')
    op.drop_table('recipe_ingredients')
    op.drop_index(op.f('ix_ingredients_name'), table_name='ingredients')
    op.drop_table('ingredients')
    op.drop_index(op.f('ix_recipes_name'), table_name='recipes')
    op.drop_table('recipes')
    op.drop_table('dietary_tags')
    op.drop_table('ingredient_categories') 