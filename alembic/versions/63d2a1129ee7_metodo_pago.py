
"""metodo_pago

Revision ID: 63d2a1129ee7
Revises: e993453c01e8
Create Date: 2025-10-20 23:52:29.601693
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '63d2a1129ee7'
down_revision: Union[str, None] = 'e993453c01e8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
