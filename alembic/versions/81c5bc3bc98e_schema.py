
"""schema

Revision ID: 81c5bc3bc98e
Revises: 201f85754b62
Create Date: 2025-10-21 00:05:40.909619
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '81c5bc3bc98e'
down_revision: Union[str, None] = '201f85754b62'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
