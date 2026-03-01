from datetime import datetime

from sqlalchemy import CheckConstraint, ForeignKey, String
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base
from src.models.mixins.primary_key import PrimaryKeyMixin
from src.models.mixins.timing import TimingMixin
from src.schemas.auth import TokenType, UserRole


class User(Base, PrimaryKeyMixin, TimingMixin):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(length=32), unique=True)
    role: Mapped[UserRole] = mapped_column(ENUM(UserRole), default=UserRole.USER)
    first_name: Mapped[str | None]
    last_name: Mapped[str | None]
    hashed_password: Mapped[str]

    __table_args__ = (CheckConstraint("length(username) <= 32", name="username_length_check"),)


class Token(Base, PrimaryKeyMixin, TimingMixin):
    __tablename__ = "tokens"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    type: Mapped[TokenType] = mapped_column(ENUM(TokenType))
    hashed_data: Mapped[str]
    expires_at: Mapped[datetime]
