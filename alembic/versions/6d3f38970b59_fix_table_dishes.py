"""fix_table_dishes

Revision ID: 6d3f38970b59
Revises: c2e770790ee2
Create Date: 2023-07-23 14:12:42.696933

"""
import sqlalchemy as sa

from alembic import op  # types: ignore

# revision identifiers, used by Alembic.
revision = '6d3f38970b59'
down_revision = 'c2e770790ee2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('dishes', sa.Column('title', sa.String(), nullable=False))
    op.add_column('dishes', sa.Column(
        'description', sa.String(), nullable=False))
    op.drop_column('dishes', 'name')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('dishes', sa.Column('name', sa.VARCHAR(),
                  autoincrement=False, nullable=False))
    op.drop_column('dishes', 'description')
    op.drop_column('dishes', 'title')
    # ### end Alembic commands ###
