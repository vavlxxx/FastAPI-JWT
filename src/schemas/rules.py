from pydantic import Field

from schemas.auth import UserRole
from src.schemas.base import BaseDTO, TimingDTO


class RuleAddDTO(BaseDTO):
    code: str
    title: str = Field(..., min_length=1, max_length=150)
    description: str | None = Field(None, min_length=1, max_length=150)
    error_message: str
    assosiated_role: UserRole


class RuleUpdateDTO(BaseDTO):
    code: str | None = None
    title: str | None = None
    description: str | None = None
    error_message: str | None = None
    assosiated_role: UserRole | None = None


class RuleDTO(RuleAddDTO, TimingDTO):
    id: int


class UserRuleAddDTO(BaseDTO):
    user_id: int
    rule_id: int


class UserRuleUpdateDTO(BaseDTO):
    user_id: int | None = None
    rule_id: int | None = None


class UserRuleDTO(UserRuleAddDTO, TimingDTO):
    id: int
