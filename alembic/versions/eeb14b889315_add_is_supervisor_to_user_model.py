"""Add is_supervisor to user model

Revision ID: eeb14b889315
Revises: 25a36669071e
Create Date: 2023-07-07 11:20:22.431946

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'eeb14b889315'
down_revision = '25a36669071e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('is_supervisor', sa.Boolean, nullable=True))

def downgrade():
    op.drop_column('users', 'is_supervisor')
