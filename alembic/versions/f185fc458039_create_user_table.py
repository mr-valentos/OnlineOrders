"""create_user_table

Revision ID: f185fc458039
Revises: 228daba84186
Create Date: 2017-03-09 17:52:44.978655

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f185fc458039'
down_revision = '228daba84186'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('login', sa.String(255), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('password', sa.String(255), nullable=False),
        sa.Column('phone', sa.String(255), nullable=False),
    )

    op.create_table(
        'roles',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
    )

    op.create_table(
        'users_roles',
        sa.Column('user_id', sa.Integer, sa.ForeignKey('user.id')),
        sa.Column('role_id', sa.Integer, sa.ForeignKey('role.id')),
    )


def downgrade():
    op.drop_table('users')
    op.drop_table('roles')
    op.drop_table('users_roles')
