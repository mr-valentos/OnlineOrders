"""create_food_table

Revision ID: 89bc9170f008
Revises: 
Create Date: 2017-03-05 16:57:14.161706

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '89bc9170f008'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'foods',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('description', sa.Text(5000), nullable=False),
        sa.Column('price', sa.DECIMAL),
        sa.Column('image', sa.String(250), nullable=True),
        sa.Column('category_id', sa.Integer, sa.ForeignKey('category.id')),
    )


def downgrade():
    op.drop_table('foods')

