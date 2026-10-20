import threading

_thread_locals = threading.local()


def get_current_request():
    return getattr(_thread_locals, "request", None)


def get_current_user():
    request = get_current_request()
    if request is not None and getattr(request, "user", None) and request.user.is_authenticated:
        return request.user
    return None


class CurrentRequestMiddleware:
    """
    Stores the current request in thread-local storage so model-layer code
    (e.g. AuditableModel save hooks, audit log signal receivers) can access
    the acting user without threading `request` through every call site.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _thread_locals.request = request
        try:
            response = self.get_response(request)
        finally:
            _thread_locals.request = None
        return response
