"""updated waste model

Revision ID: 621e7cd8c93a
Revises: e1c27b1aa194
Create Date: 2024-04-21 15:27:30.011202

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel



# revision identifiers, used by Alembic.
revision: str = '621e7cd8c93a'
down_revision: Union[str, None] = 'e1c27b1aa194'
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