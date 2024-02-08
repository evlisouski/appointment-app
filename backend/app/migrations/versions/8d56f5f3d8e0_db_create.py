"""DB create

Revision ID: 8d56f5f3d8e0
Revises: 
Create Date: 2024-02-05 01:01:13.303425

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8d56f5f3d8e0'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('customers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=256), nullable=False),
    sa.Column('birthday', sa.Date(), nullable=True),
    sa.Column('registration_date', sa.Date(), nullable=False),
    sa.Column('rating', sa.SmallInteger(), nullable=True),
    sa.Column('verified', sa.Boolean(), nullable=False),
    sa.Column('location', sa.String(), nullable=False),
    sa.Column('image_id', sa.Integer(), nullable=True),
    sa.Column('score', sa.SmallInteger(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('providers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=256), nullable=False),
    sa.Column('foundation_date', sa.Date(), nullable=True),
    sa.Column('registration_date', sa.Date(), nullable=False),
    sa.Column('rating', sa.SmallInteger(), nullable=True),
    sa.Column('verified', sa.Boolean(), nullable=False),
    sa.Column('location', sa.String(), nullable=False),
    sa.Column('image_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tags',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('providers_tags',
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.Column('provider_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['provider_id'], ['providers.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], ),
    sa.PrimaryKeyConstraint('tag_id', 'provider_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('providers_tags')
    op.drop_table('tags')
    op.drop_table('providers')
    op.drop_table('customers')
    # ### end Alembic commands ###