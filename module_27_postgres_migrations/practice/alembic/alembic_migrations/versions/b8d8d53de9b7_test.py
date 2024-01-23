"""test

Revision ID: b8d8d53de9b7
Revises: 7cfad84f1d09
Create Date: 2024-01-22 20:24:52.914611

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b8d8d53de9b7'
down_revision: Union[str, None] = '7cfad84f1d09'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
