FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        curl \
        gettext \
    && rm -rf /var/lib/apt/lists/*

RUN addgroup --system django && adduser --system --ingroup django django

WORKDIR /app

COPY requirements/ requirements/
ARG BUILD_ENV=production
RUN pip install -r requirements/${BUILD_ENV}.txt

COPY . .

RUN mkdir -p /app/logs /app/staticfiles /app/media \
    && chown -R django:django /app

USER django

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:8000/api/schema/ || exit 1

# Daphne serves the full ASGI app (HTTP + WebSocket) behind Nginx, since
# Channels needs an ASGI server rather than the WSGI-only gunicorn workers.
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "config.asgi:application"]
