"""create_food_order_table

Revision ID: a174fbf39386
Revises: 121d6f3e0910
Create Date: 2017-03-21 22:52:15.918866

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a174fbf39386'
down_revision = '121d6f3e0910'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'food_orders',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('order_id', sa.Integer, sa.ForeignKey('order.id'), nullable=False),
        sa.Column('food_id', sa.Integer, sa.ForeignKey('food.id')),
        sa.Column('count', sa.Integer),
        sa.Column('price', sa.Integer)
    )


def downgrade():
    op.drop_table('food_orders')