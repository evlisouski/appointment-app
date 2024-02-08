"""dsf

Revision ID: cad8108c26f1
Revises: 8d56f5f3d8e0
Create Date: 2024-02-05 01:23:45.437142

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cad8108c26f1'
down_revision: Union[str, None] = '8d56f5f3d8e0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('left_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('right_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('association_table',
    sa.Column('left_id', sa.Integer(), nullable=False),
    sa.Column('right_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['left_id'], ['left_table.id'], ),
    sa.ForeignKeyConstraint(['right_id'], ['right_table.id'], ),
    sa.PrimaryKeyConstraint('left_id', 'right_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('association_table')
    op.drop_table('right_table')
    op.drop_table('left_table')
    # ### end Alembic commands ###