import sqlmodel
"""add phone number to users table

Revision ID: 86340dc3b7bb
Revises: b3ae26013d6e
Create Date: 2024-11-20 14:46:16.624225

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '86340dc3b7bb'
down_revision: Union[str, None] = 'b3ae26013d6e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        "users",
        sa.Column("phone_number", sa.String, nullable=True)
    )


def downgrade():
    op.drop_column("users", "phone_number")
