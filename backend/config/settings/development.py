from .base import *  # noqa: F401,F403
from .base import INSTALLED_APPS, MIDDLEWARE, env

DEBUG = True

INSTALLED_APPS += ["django_extensions"]

if env.bool("ENABLE_DEBUG_TOOLBAR", default=False):
    INSTALLED_APPS += ["debug_toolbar"]
    MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"] + MIDDLEWARE
    INTERNAL_IPS = ["127.0.0.1"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

CORS_ALLOW_ALL_ORIGINS = True

# Redis isn't running in this local dev environment (no Docker, no native
# install) -- fall back to in-process backends so caching (and the
# ScopedRateThrottle "auth"/"otp" scopes, which read the default cache) and
# channel layers work without it. production.py / docker-compose keep the
# real Redis-backed CACHES/CHANNEL_LAYERS from base.py.
CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}
CHANNEL_LAYERS = {"default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}}

# Relaxed for local http development only — production.py enforces HTTPS.
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
