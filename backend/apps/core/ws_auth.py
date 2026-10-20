from urllib.parse import parse_qs

from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import AccessToken


@database_sync_to_async
def _get_user_from_token(token: str):
    from django.contrib.auth import get_user_model

    try:
        validated = AccessToken(token)
        user_id = validated["user_id"]
    except (InvalidToken, TokenError, KeyError):
        return AnonymousUser()

    User = get_user_model()
    try:
        user = User.objects.get(id=user_id, is_active=True)
    except User.DoesNotExist:
        return AnonymousUser()
    return user


class JWTAuthMiddleware(BaseMiddleware):
    """
    Authenticates WebSocket connections using the same JWT access tokens
    issued for REST API calls, passed as ?token=<access_token> on the
    connection URL (browsers cannot set custom headers on WS handshakes).
    """

    async def __call__(self, scope, receive, send):
        query_string = parse_qs(scope["query_string"].decode())
        token = query_string.get("token", [None])[0]
        scope["user"] = await _get_user_from_token(token) if token else AnonymousUser()
        return await super().__call__(scope, receive, send)


def JWTAuthMiddlewareStack(inner):
    return JWTAuthMiddleware(AuthMiddlewareStack(inner))
