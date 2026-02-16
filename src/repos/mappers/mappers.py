from src.models.auth import Token, User
from src.models.rules import Rule, UserRule
from src.repos.mappers.base import DataMapper
from src.schemas.auth import TokenDTO, UserDTO
from src.schemas.rules import RuleDTO, UserRuleDTO


class AuthMapper(DataMapper[User, UserDTO]):
    model = User
    schema = UserDTO


class TokenMapper(DataMapper[Token, TokenDTO]):
    model = Token
    schema = TokenDTO


class RuleMapper(DataMapper[Rule, RuleDTO]):
    model = Rule
    schema = RuleDTO


class UserRuleMapper(DataMapper[UserRule, UserRuleDTO]):
    model = UserRule
    schema = UserRuleDTO
