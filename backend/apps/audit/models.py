from django.conf import settings
from django.db import models

from apps.core.models import TimeStampedModel, UUIDPublicIDModel


class AuditAction(models.TextChoices):
    LOGIN_SUCCESS = "login_success", "Login Success"
    LOGIN_FAILED = "login_failed", "Login Failed"
    LOGOUT = "logout", "Logout"
    MFA_CHALLENGE_SENT = "mfa_challenge_sent", "MFA Challenge Sent"
    MFA_VERIFIED = "mfa_verified", "MFA Verified"
    MFA_FAILED = "mfa_failed", "MFA Failed"
    MFA_ENABLED = "mfa_enabled", "MFA Enabled"
    MFA_DISABLED = "mfa_disabled", "MFA Disabled"
    PASSWORD_CHANGED = "password_changed", "Password Changed"
    PASSWORD_RESET_REQUESTED = "password_reset_requested", "Password Reset Requested"
    PASSWORD_RESET_COMPLETED = "password_reset_completed", "Password Reset Completed"
    ACCOUNT_LOCKED = "account_locked", "Account Locked"
    PERMISSION_DENIED = "permission_denied", "Permission Denied"
    RECORD_CREATED = "record_created", "Record Created"
    RECORD_UPDATED = "record_updated", "Record Updated"
    RECORD_DELETED = "record_deleted", "Record Deleted"
    SENSITIVE_DATA_VIEWED = "sensitive_data_viewed", "Sensitive Data Viewed"
    DATA_EXPORTED = "data_exported", "Data Exported"
    API_REQUEST = "api_request", "API Request"


class AuditSeverity(models.TextChoices):
    INFO = "info", "Info"
    WARNING = "warning", "Warning"
    CRITICAL = "critical", "Critical"


class AuditLog(TimeStampedModel, UUIDPublicIDModel):
    """
    Immutable, append-only audit trail satisfying HIPAA/HL7-style access
    logging requirements: who did what, to which record, from where, and
    when. Never updated after creation and never hard-deleted by application
    code -- only the scheduled archival task moves old rows to cold storage.
    """

    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="audit_logs",
        help_text="Null for unauthenticated events (e.g. failed login with unknown user).",
    )
    actor_email_snapshot = models.EmailField(blank=True)
    branch = models.ForeignKey("branches.Branch", null=True, blank=True, on_delete=models.SET_NULL)

    action = models.CharField(max_length=40, choices=AuditAction.choices, db_index=True)
    severity = models.CharField(max_length=10, choices=AuditSeverity.choices, default=AuditSeverity.INFO)

    target_model = models.CharField(max_length=100, blank=True, db_index=True)
    target_object_id = models.CharField(max_length=64, blank=True, db_index=True)
    target_repr = models.CharField(max_length=255, blank=True)
    changes = models.JSONField(default=dict, blank=True, help_text="Before/after field diff for update actions.")

    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=500, blank=True)
    request_method = models.CharField(max_length=10, blank=True)
    request_path = models.CharField(max_length=500, blank=True)
    status_code = models.PositiveSmallIntegerField(null=True, blank=True)
    duration_ms = models.PositiveIntegerField(null=True, blank=True)

    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["actor", "created_at"]),
            models.Index(fields=["target_model", "target_object_id"]),
            models.Index(fields=["action", "created_at"]),
        ]

    def __str__(self) -> str:
        who = self.actor_email_snapshot or "system"
        return f"[{self.created_at:%Y-%m-%d %H:%M:%S}] {who} - {self.action}"

    def save(self, *args, **kwargs):
        if self.pk is not None:
            raise ValueError("AuditLog records are immutable and cannot be updated after creation.")
        super().save(*args, **kwargs)
