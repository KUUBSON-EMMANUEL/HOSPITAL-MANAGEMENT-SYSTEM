import logging
import time

from apps.core.utils import get_client_ip

from .models import AuditAction, AuditLog, AuditSeverity

logger = logging.getLogger("hms.audit")

_EXCLUDED_PREFIXES = ("/static/", "/media/", "/admin/jsi18n/", "/__debug__/")


class AuditLogMiddleware:
    """
    Writes one generic AuditLog row per request (action=API_REQUEST).
    Semantic business events (LOGIN_SUCCESS, MFA_VERIFIED, etc.) are logged
    explicitly by the views that perform them -- this middleware is the
    catch-all request trail, not a replacement for those.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.monotonic()
        response = self.get_response(request)

        if request.path.startswith(_EXCLUDED_PREFIXES):
            return response

        try:
            user = getattr(request, "user", None)
            actor = user if user and user.is_authenticated else None
            AuditLog.objects.create(
                actor=actor,
                actor_email_snapshot=actor.email if actor else "",
                branch=getattr(actor, "branch", None) if actor else None,
                action=AuditAction.API_REQUEST,
                severity=AuditSeverity.WARNING if response.status_code >= 400 else AuditSeverity.INFO,
                ip_address=get_client_ip(request),
                user_agent=request.META.get("HTTP_USER_AGENT", "")[:500],
                request_method=request.method,
                request_path=request.path[:500],
                status_code=response.status_code,
                duration_ms=int((time.monotonic() - start) * 1000),
            )
        except Exception:
            logger.exception("audit_log_write_failed")

        return response
