"""changed the customer id to auto-incremental

Revision ID: 55593e5d74e5
Revises: 9b2fd90a04ec
Create Date: 2024-02-12 13:06:34.045733

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '55593e5d74e5'
down_revision: Union[str, None] = '9b2fd90a04ec'
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
