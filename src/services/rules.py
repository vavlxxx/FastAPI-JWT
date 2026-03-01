from typing import List

from src.schemas.rules import RuleAddDTO
from src.services.base import BaseService


class RuleService(BaseService):
    def has_rule(
        self,
        uid: int,
        code: str,
    ) -> bool: ...

    def create_rules(
        self,
        uid: int,
        rule: List[RuleAddDTO],
    ) -> int: ...

    def add_rule_to_user(
        self,
        uid: int,
        code: str,
    ) -> None: ...

    def remove_rule_from_user(
        self,
        uid: int,
        code: str,
    ) -> None: ...
