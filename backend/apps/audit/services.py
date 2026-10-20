from typing import Any

from .models import AuditAction, AuditLog, AuditSeverity


def log_action(
    *,
    action: AuditAction,
    actor=None,
    request=None,
    target=None,
    changes: dict | None = None,
    severity: str = AuditSeverity.INFO,
    metadata: dict[str, Any] | None = None,
) -> AuditLog:
    """
    Records a single audit event. Written synchronously (not via Celery) so
    the audit trail's durability never depends on the message broker being
    up -- compliance logging must not be best-effort.
    """
    ip_address = None
    user_agent = ""
    request_method = ""
    request_path = ""

    if request is not None:
        ip_address = _client_ip(request)
        user_agent = request.META.get("HTTP_USER_AGENT", "")[:500]
        request_method = request.method
        request_path = request.path[:500]
        if actor is None and getattr(request, "user", None) and request.user.is_authenticated:
            actor = request.user

    branch = getattr(actor, "branch", None) if actor is not None else None

    return AuditLog.objects.create(
        actor=actor,
        actor_email_snapshot=getattr(actor, "email", ""),
        branch=branch,
        action=action,
        severity=severity,
        target_model=target.__class__.__name__ if target is not None else "",
        target_object_id=str(getattr(target, "pk", "")) if target is not None else "",
        target_repr=str(target)[:255] if target is not None else "",
        changes=changes or {},
        ip_address=ip_address,
        user_agent=user_agent,
        request_method=request_method,
        request_path=request_path,
        metadata=metadata or {},
    )


def _client_ip(request) -> str | None:
    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")
