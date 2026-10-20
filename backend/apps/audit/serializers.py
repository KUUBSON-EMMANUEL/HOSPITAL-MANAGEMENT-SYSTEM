from rest_framework import serializers

from apps.core.serializers import PublicIdRelatedField

from .models import AuditLog


class AuditLogSerializer(serializers.ModelSerializer):
    actor = PublicIdRelatedField(read_only=True)
    branch = PublicIdRelatedField(read_only=True)

    class Meta:
        model = AuditLog
        fields = [
            "public_id", "actor", "actor_email_snapshot", "branch", "action", "severity",
            "target_model", "target_object_id", "target_repr", "changes",
            "ip_address", "user_agent", "request_method", "request_path", "status_code", "duration_ms",
            "metadata", "created_at",
        ]
        read_only_fields = fields
