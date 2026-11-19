
"""add priority column to tasks

Revision ID: efa971e5c846
Revises: 704f6a1df73d
Create Date: 2026-11-14 14:39:07.653225

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'efa971e5c846'
down_revision: Union[str, Sequence[str], None] = '704f6a1df73d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # Add priority column with a temporary default
    op.add_column(
        'tasks',
        sa.Column(
            'priority',
            sa.String(length=20),
            nullable=False,
            server_default=sa.text("'normal'")
        )
    )

    # Remove database-level default after existing rows are updated
    op.alter_column(
        'tasks',
        'priority',
        server_default=None
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column('tasks', 'priority')