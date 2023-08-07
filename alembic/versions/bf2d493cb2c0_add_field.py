"""add_field

Revision ID: bf2d493cb2c0
Revises: d1749e36d326
Create Date: 2023-07-23 11:57:24.074062

"""
import sqlalchemy as sa

from alembic import op  # types: ignore

# revision identifiers, used by Alembic.
revision = 'bf2d493cb2c0'
down_revision = 'd1749e36d326'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('main_menu', sa.Column('title', sa.String(), nullable=False))
    op.add_column('main_menu', sa.Column(
        'description', sa.String(), nullable=False))
    op.drop_column('main_menu', 'name')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('main_menu', sa.Column(
        'name', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column('main_menu', 'description')
    op.drop_column('main_menu', 'title')
    # ### end Alembic commands ###
