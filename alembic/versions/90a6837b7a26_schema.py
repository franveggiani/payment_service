
"""schema

Revision ID: 90a6837b7a26
Revises: 81c5bc3bc98e
Create Date: 2025-10-21 00:08:31.756227
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '90a6837b7a26'
down_revision: Union[str, None] = '81c5bc3bc98e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
