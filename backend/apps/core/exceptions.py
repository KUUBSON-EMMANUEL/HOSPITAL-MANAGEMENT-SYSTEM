import logging
import uuid

from rest_framework.response import Response
from rest_framework.views import exception_handler

logger = logging.getLogger("hms.audit")


class DomainError(Exception):
    """Base class for expected business-rule violations raised by services."""

    default_message = "The request could not be completed."
    code = "domain_error"

    def __init__(self, message: str | None = None, code: str | None = None):
        self.message = message or self.default_message
        self.code = code or self.code
        super().__init__(self.message)


def custom_exception_handler(exc, context):
    """
    Wraps DRF's default exception handler to:
      - return a consistent {error: {code, message, request_id}} envelope
      - log every 4xx/5xx with a correlation id for audit/traceability
      - never leak internal exception details to clients
    """
    response = exception_handler(exc, context)
    request_id = str(uuid.uuid4())

    if isinstance(exc, DomainError):
        logger.warning("domain_error", extra={"request_id": request_id, "code": exc.code, "message": exc.message})
        return Response(
            {"error": {"code": exc.code, "message": exc.message, "request_id": request_id}},
            status=422,
        )

    if response is not None:
        logger.warning(
            "api_error",
            extra={
                "request_id": request_id,
                "status_code": response.status_code,
                "detail": response.data,
                "path": context["request"].path if context.get("request") else None,
            },
        )
        response.data = {
            "error": {
                "code": getattr(exc, "default_code", "error"),
                "message": response.data,
                "request_id": request_id,
            }
        }
        return response

    logger.error("unhandled_exception", exc_info=exc, extra={"request_id": request_id})
    return None
