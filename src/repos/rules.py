from sqlalchemy import delete, select

from src.models.rules import Rule, UserRule
from src.repos.base import BaseRepo
from src.repos.mappers.mappers import (
    RuleMapper,
    UserRuleMapper,
)
from src.schemas.rules import (
    RuleAddDTO,
    RuleDTO,
    RuleUpdateDTO,
    UserRuleAddDTO,
    UserRuleDTO,
    UserRuleUpdateDTO,
)


class RulesRepo(
    BaseRepo[
        Rule,
        RuleDTO,
        RuleAddDTO,
        RuleUpdateDTO,
    ]
):
    model = Rule
    schema = RuleDTO
    mapper = RuleMapper


class UserRulesRepo(
    BaseRepo[
        UserRule,
        UserRuleDTO,
        UserRuleAddDTO,
        UserRuleUpdateDTO,
    ]
):
    model = UserRule
    schema = UserRuleDTO
    mapper = UserRuleMapper

    async def get_user_rules(
        self, *filter, user_id: int, **filter_by
    ) -> list[UserRuleDTO]:
        query = (
            select(UserRule)
            .join(Rule, UserRule.rule_id == Rule.id)
            .filter(*filter)
            .filter_by(
                user_id=user_id,
                **filter_by,
            )
        )
        result = await self.session.execute(query)
        rules = result.scalars().all()
        return [
            self.mapper.map_to_domain_entity(item)
            for item in rules
        ]

    async def assign_rules(
        self,
        user_id: int,
        codes: list[str],
    ):
        query = select(Rule).filter(Rule.code.in_(codes))
        result = await self.session.execute(query)
        rules = [
            RuleMapper.map_to_domain_entity(item)
            for item in result.scalars().all()
        ]

        data = [
            UserRuleAddDTO(
                user_id=user_id,
                rule_id=rule.id,
            )
            for rule in rules
        ]
        return await self.add_bulk(data)

    async def unassign_rules(
        self,
        user_id: int,
        codes: list[str],
    ):
        stmt = delete(self.model).where(
            self.model.id.in_(
                select(UserRule.id)
                .where(UserRule.rule_id == Rule.id)
                .where(Rule.code.in_(codes))
                .where(UserRule.user_id == user_id)
            )
        )
        await self.session.execute(stmt)
