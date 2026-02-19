from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base
from src.models.mixins.primary_key import PrimaryKeyMixin
from src.models.mixins.timing import TimingMixin
from src.schemas.auth import UserRole


class Rule(Base, PrimaryKeyMixin, TimingMixin):
    __tablename__ = "rules"

    assosiated_role: Mapped[UserRole | None] = (
        mapped_column(ENUM(UserRole), nullable=True)
    )
    code: Mapped[str] = mapped_column(unique=True)
    title: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str | None]
    error_message: Mapped[str]


class UserRule(Base, PrimaryKeyMixin, TimingMixin):
    __tablename__ = "user_rules"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )
    rule_id: Mapped[int] = mapped_column(
        ForeignKey("rules.id")
    )

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "rule_id",
            name="user_assosiated_rule_unique",
        ),
    )
