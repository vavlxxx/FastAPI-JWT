from src.models.auth import Token
from src.models.rules import Rule
from src.repos.base import BaseRepo
from src.repos.mappers.mappers import RuleMapper, TokenMapper
from src.schemas.auth import (
    TokenAddDTO,
    TokenDTO,
    TokenUpdateDTO,
)
from src.schemas.rules import RuleAddDTO, RuleDTO, RuleUpdateDTO


class RulesRepo(BaseRepo[Rule, RuleDTO, RuleAddDTO, RuleUpdateDTO]):
    model = Rule
    schema = RuleDTO
    mapper = RuleMapper


class TokenRepo(BaseRepo[Token, TokenDTO, TokenAddDTO, TokenUpdateDTO]):
    model = Token
    schema = TokenDTO
    mapper = TokenMapper
