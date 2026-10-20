from channels.routing import URLRouter

from apps.messaging.routing import websocket_urlpatterns as messaging_ws
from apps.notifications.routing import websocket_urlpatterns as notifications_ws

websocket_urlpatterns = [
    *notifications_ws,
    *messaging_ws,
]

websocket_router = URLRouter(websocket_urlpatterns)
