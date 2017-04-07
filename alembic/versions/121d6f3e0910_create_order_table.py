"""create_order_table

Revision ID: 121d6f3e0910
Revises: f185fc458039
Create Date: 2017-03-18 02:30:41.951703

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '121d6f3e0910'
down_revision = 'f185fc458039'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'orders',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('address', sa.String(50)),
        sa.Column('created_at', sa.DateTime),
        sa.Column('time', sa.DateTime),
        sa.Column('user_id', sa.Integer, sa.ForeignKey("user.id")),
        sa.Column('status', sa.String(255), nullable=False)
    )


def downgrade():
    op.drop_table('orders')