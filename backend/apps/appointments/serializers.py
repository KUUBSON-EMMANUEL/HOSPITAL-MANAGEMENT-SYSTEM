from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.branches.models import Branch
from apps.core.serializers import PublicIdRelatedField
from apps.patients.models import Patient

from .models import Appointment

User = get_user_model()


class AppointmentSerializer(serializers.ModelSerializer):
    branch = PublicIdRelatedField(queryset=Branch.objects.all())
    patient = PublicIdRelatedField(queryset=Patient.objects.all())
    provider = PublicIdRelatedField(queryset=User.objects.all())

    class Meta:
        model = Appointment
        fields = [
            "public_id", "branch", "patient", "provider", "module", "appointment_type",
            "scheduled_start", "scheduled_end", "status", "reason", "cancellation_reason",
            "created_at", "updated_at",
        ]
        read_only_fields = ["public_id", "created_at", "updated_at"]

    def validate(self, attrs):
        start = attrs.get("scheduled_start", getattr(self.instance, "scheduled_start", None))
        end = attrs.get("scheduled_end", getattr(self.instance, "scheduled_end", None))
        if start and end and end <= start:
            raise serializers.ValidationError({"scheduled_end": "Must be after scheduled_start."})
        # TODO: double-booking validation (no two appointments for the same
        # provider with overlapping [scheduled_start, scheduled_end)) is not
        # enforced yet -- planned as a follow-up service-layer check.
        return attrs
