"""added rules system

Revision ID: 7a5dea6eb433
Revises: 2094603e316e
Create Date: 2026-02-16 11:20:40.258593

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "7a5dea6eb433"
down_revision: Union[str, Sequence[str], None] = (
    "2094603e316e"
)
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "rules",
        sa.Column(
            "id",
            sa.Integer(),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column(
            "assosiated_role",
            postgresql.ENUM(
                "SUPERUSER",
                "ADMIN",
                "USER",
                name="userrole",
                create_type=False,
            ),
            nullable=True,
        ),
        sa.Column("code", sa.String(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column(
            "description", sa.String(), nullable=True
        ),
        sa.Column(
            "error_message", sa.String(), nullable=False
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint(
            "id", name=op.f("pk_rules")
        ),
        sa.UniqueConstraint(
            "code", name=op.f("uq_rules_code")
        ),
        sa.UniqueConstraint(
            "title", name=op.f("uq_rules_title")
        ),
    )
    op.create_table(
        "user_rules",
        sa.Column(
            "id",
            sa.Integer(),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("rule_id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["rule_id"],
            ["rules.id"],
            name=op.f("fk_user_rules_rule_id_rules"),
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_user_rules_user_id_users"),
        ),
        sa.PrimaryKeyConstraint(
            "id", name=op.f("pk_user_rules")
        ),
        sa.UniqueConstraint(
            "user_id",
            "rule_id",
            name="user_assosiated_rule_unique",
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("user_rules")
    op.drop_table("rules")
