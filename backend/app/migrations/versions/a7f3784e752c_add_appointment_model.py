"""Add Appointment model

Revision ID: a7f3784e752c
Revises: e03c092e1f9a
Create Date: 2024-02-18 21:31:03.489682

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a7f3784e752c'
down_revision: Union[str, None] = 'e03c092e1f9a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('appointments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('provider_id', sa.Integer(), nullable=False),
    sa.Column('customer_id', sa.BigInteger(), nullable=True),
    sa.Column('offer', sa.String(), nullable=False),
    sa.Column('datetime_from', sa.DateTime(), nullable=False),
    sa.Column('datetime_to', sa.DateTime(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['provider_id'], ['providers.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', 'provider_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('appointments')
    # ### end Alembic commands ###