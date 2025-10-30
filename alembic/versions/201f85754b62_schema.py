
"""schema

Revision ID: 201f85754b62
Revises: 63d2a1129ee7
Create Date: 2025-10-21 00:02:21.945075
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '201f85754b62'
down_revision: Union[str, None] = '63d2a1129ee7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
