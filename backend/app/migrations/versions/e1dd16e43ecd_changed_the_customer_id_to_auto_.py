"""changed the customer id to auto-incremental

Revision ID: e1dd16e43ecd
Revises: 55593e5d74e5
Create Date: 2024-02-12 13:12:20.866733

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e1dd16e43ecd'
down_revision: Union[str, None] = '55593e5d74e5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
