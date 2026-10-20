def get_client_ip(request):
    """Prefers X-Forwarded-For (set by nginx in front of the app) over REMOTE_ADDR."""
    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")
