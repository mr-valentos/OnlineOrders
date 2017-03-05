"""create_category_table

Revision ID: 228daba84186
Revises: 89bc9170f008
Create Date: 2017-03-05 16:59:13.591865

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '228daba84186'
down_revision = '89bc9170f008'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'categories',
        sa.Column('id', sa.Integer, primary_key=True, ),
        sa.Column('name', sa.String(50), nullable=False),
    )


def downgrade():
    op.drop_table('categories')
