from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from rest_framework import serializers

from apps.branches.models import Branch
from apps.core.serializers import PublicIdRelatedField
from apps.patients.models import Patient

from .models import INACTIVE_STATUSES, Appointment

DOUBLE_BOOKING_MESSAGE = "This provider already has an appointment that overlaps this time."

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
        provider = attrs.get("provider", getattr(self.instance, "provider", None))
        status = attrs.get("status", getattr(self.instance, "status", Appointment.Status.SCHEDULED))
        if start and end and provider and status not in INACTIVE_STATUSES:
            overlapping = Appointment.objects.filter(
                provider=provider, scheduled_start__lt=end, scheduled_end__gt=start
            ).exclude(status__in=INACTIVE_STATUSES)
            if self.instance is not None:
                overlapping = overlapping.exclude(pk=self.instance.pk)
            if overlapping.exists():
                raise serializers.ValidationError({"scheduled_start": DOUBLE_BOOKING_MESSAGE})
        return attrs

    # The exclusion constraint on Appointment catches the race where two
    # requests pass validate() at the same moment; report it as a 400.
    def create(self, validated_data):
        try:
            with transaction.atomic():
                return super().create(validated_data)
        except IntegrityError as exc:
            if "appointment_no_provider_overlap" in str(exc):
                raise serializers.ValidationError({"scheduled_start": DOUBLE_BOOKING_MESSAGE}) from exc
            raise

    def update(self, instance, validated_data):
        try:
            with transaction.atomic():
                return super().update(instance, validated_data)
        except IntegrityError as exc:
            if "appointment_no_provider_overlap" in str(exc):
                raise serializers.ValidationError({"scheduled_start": DOUBLE_BOOKING_MESSAGE}) from exc
            raise
