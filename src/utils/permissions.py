from abc import ABC, abstractmethod
from typing import Iterable

from fastapi import status
from starlette.requests import Request

from src.api.v1.dependencies.auth import GetUserDTO
from src.schemas.auth import UserDTO, UserRole
from src.utils.exceptions import NotEnoughPermissionsHTTPError


class BasePermission(ABC):
    error_msg = "You cannot perform this action"
    error_code = status.HTTP_403_FORBIDDEN

    @abstractmethod
    def has_permission(self, request: Request, current_user: UserDTO) -> bool:
        pass

    def __call__(self, request: Request, current_user: GetUserDTO):
        if not self.has_permission(request, current_user):
            raise NotEnoughPermissionsHTTPError(status_code=self.error_code, detail=self.error_msg)


def any_permission(request: Request, permissions: Iterable[BasePermission], current_user: UserDTO) -> bool:
    for permission_class in permissions:
        try:
            perm = permission_class()  # pyright: ignore
            if perm.has_permission(request, current_user):
                return True
        except NotEnoughPermissionsHTTPError:
            pass
    return False


class IsAdminPermission(BasePermission):
    error_msg = "Only admins allowed to perform this action"

    def has_permission(self, request: Request, current_user) -> bool:
        return current_user.role == UserRole.ADMIN


class IsUserPermission(BasePermission):
    error_msg = "Only users allowed to perform this action"

    def has_permission(self, request: Request, current_user) -> bool:
        return current_user.role == UserRole.USER


class IsSuperuserPermission(BasePermission):
    error_msg = "Only superuser allowed to perform this action"

    def has_permission(self, request: Request, current_user) -> bool:
        return current_user.role == UserRole.SUPERUSER
