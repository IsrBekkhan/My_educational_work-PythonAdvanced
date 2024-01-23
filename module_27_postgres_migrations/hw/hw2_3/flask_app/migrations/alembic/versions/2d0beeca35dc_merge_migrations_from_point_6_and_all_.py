"""merge migrations from point 6 and all other points

Revision ID: 2d0beeca35dc
Revises: 78ac8e3e2d61, 8cf370f00c85
Create Date: 2024-01-22 21:29:10.087272

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2d0beeca35dc'
down_revision: Union[str, None] = ('78ac8e3e2d61', '8cf370f00c85')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
