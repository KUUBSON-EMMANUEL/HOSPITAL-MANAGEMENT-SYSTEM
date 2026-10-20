from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.branches.models import Branch
from apps.core.serializers import PublicIdRelatedField
from apps.patients.models import Patient

from .models import EmergencyCase

User = get_user_model()


class EmergencyCaseSerializer(serializers.ModelSerializer):
    branch = PublicIdRelatedField(queryset=Branch.objects.all())
    patient = PublicIdRelatedField(queryset=Patient.objects.all())
    attending_provider = PublicIdRelatedField(queryset=User.objects.all(), required=False, allow_null=True)

    class Meta:
        model = EmergencyCase
        fields = [
            "public_id", "branch", "patient", "triage_level", "arrival_time", "chief_complaint",
            "status", "attending_provider", "created_at", "updated_at",
        ]
        read_only_fields = ["public_id", "arrival_time", "created_at", "updated_at"]
