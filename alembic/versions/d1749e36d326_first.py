"""first

Revision ID: d1749e36d326
Revises:
Create Date: 2023-07-22 16:09:40.348933

"""
import sqlalchemy as sa

from alembic import op  # types: ignore

# revision identifiers, used by Alembic.
revision = 'd1749e36d326'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('main_menu',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('sub_menu',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('main_menu_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(
                        ['main_menu_id'], ['main_menu.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('dishes',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('sub_menu_id', sa.Integer(), nullable=False),
                    sa.Column('price', sa.Numeric(
                        precision=18, scale=2), nullable=True),
                    sa.ForeignKeyConstraint(
                        ['sub_menu_id'], ['sub_menu.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('dishes')
    op.drop_table('sub_menu')
    op.drop_table('main_menu')
    # ### end Alembic commands ###
