from typing import List

from src.schemas.rules import (
    RuleAddDTO,
    RuleDTO,
    UserRuleDTO,
)
from src.services.base import BaseService


class RuleService(BaseService):
    async def has_rule(
        self,
        uid: int,
        code: str,
    ) -> bool:
        user_rule = await self.db.user_rules.get_user_rules(
            user_id=uid,
            code=code,
        )
        return bool(user_rule)

    async def add_rules(
        self,
        rules: List[RuleAddDTO],
    ) -> list[RuleDTO]:
        added_rules = await self.db.rules.add_bulk(
            data=rules,
        )
        return added_rules

    async def assign_rules_for_user(
        self,
        uid: int,
        codes: list[str],
    ) -> list[UserRuleDTO]:
        user_rules = await self.db.user_rules.assign_rules(
            user_id=uid,
            codes=codes,
        )
        return user_rules

    async def unassign_rules_for_user(
        self,
        uid: int,
        codes: list[str],
    ) -> None:
        await self.db.user_rules.unassign_rules(
            user_id=uid,
            codes=codes,
        )
