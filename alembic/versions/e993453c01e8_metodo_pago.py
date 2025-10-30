
"""metodo_pago

Revision ID: e993453c01e8
Revises: cc63b36ee6d0
Create Date: 2025-10-20 23:50:20.913663
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e993453c01e8'
down_revision: Union[str, None] = 'cc63b36ee6d0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
