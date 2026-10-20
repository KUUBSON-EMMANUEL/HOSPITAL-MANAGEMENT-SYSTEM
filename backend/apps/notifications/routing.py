"""
WebSocket routes for the notifications module.
Populated when the Notification System module is implemented; the real-time
architecture (ASGI app, Redis channel layer) is already wired up in
config/asgi.py and config/routing.py.
"""

websocket_urlpatterns: list = []
