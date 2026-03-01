"""added basic role model

Revision ID: 2094603e316e
Revises: 8093419d4e91
Create Date: 2026-02-15 21:52:26.033668

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "2094603e316e"
down_revision: Union[str, Sequence[str], None] = "8093419d4e91"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("DROP TYPE IF EXISTS userrole")
    user_role_enum = postgresql.ENUM("SUPERUSER", "ADMIN", "USER", name="userrole")
    user_role_enum.create(op.get_bind())

    op.add_column(
        "users",
        sa.Column(
            "role",
            user_role_enum,
            server_default="USER",
            nullable=False,
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users", "role")
    op.execute("DROP TYPE IF EXISTS userrole")
