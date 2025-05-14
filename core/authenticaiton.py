from typing import Any, Optional

from django.http import HttpRequest
from ninja.errors import HttpError
from ninja.security import HttpBearer


class _BaseAuth(HttpBearer):
    def authenticate(self, request: HttpRequest, token: str):
        if len(token.split(" ")) != 1:
            raise HttpError(message="Invalid Authentication header ( bearer <Token> ).", status_code=401)


# class AnonymousUserAuth(_BaseAuth):
#     def authenticate(self, request: HttpRequest, token: str) -> Optional[Any]:
#         super().authenticate(request, token)
#
#         try:
#             profile = Profile.objects.select_related('user__teacher').get(token=token)
#             request.user = profile.user
#             request.profile = profile
#             request.is_authenticated = request.profile.is_authenticated
#             return profile
#         except Profile.DoesNotExist:
#             pass


# class AuthenticatedUserAuth(_BaseAuth):
#     def authenticate(self, request: HttpRequest, token: str) -> Optional[Any]:
#         super().authenticate(request, token)
#
#         try:
#             profile = (
#                 Profile.objects.authenticated_users()
#                 .select_related('user__teacher')
#                 .get(token=token)
#             )
#             if profile.user.is_active:
#                 request.user = profile.user
#                 request.profile = profile
#                 request.is_authenticated = request.profile.is_authenticated
#                 return profile
#         except Profile.DoesNotExist:
#             pass
