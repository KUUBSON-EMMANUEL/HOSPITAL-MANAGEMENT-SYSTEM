import os

from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")

# django_asgi_app must be constructed before importing anything that touches
# models/routing, so Django's app registry is populated first.
django_asgi_app = get_asgi_application()

from apps.core.ws_auth import JWTAuthMiddlewareStack  # noqa: E402
from config.routing import websocket_router  # noqa: E402

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": JWTAuthMiddlewareStack(websocket_router),
    }
)
