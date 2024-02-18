"""empty message

Revision ID: 84016f59eeb5
Revises: 73c5a280f808
Create Date: 2024-02-16 19:10:30.925008

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '84016f59eeb5'
down_revision: Union[str, None] = '73c5a280f808'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('providers_user_id_fkey', 'providers', type_='foreignkey')
    op.drop_column('providers', 'user_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('providers', sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('providers_user_id_fkey', 'providers', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###