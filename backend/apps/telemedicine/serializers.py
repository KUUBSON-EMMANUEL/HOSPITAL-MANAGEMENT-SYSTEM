from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.branches.models import Branch
from apps.core.serializers import PublicIdRelatedField
from apps.patients.models import Patient

from .models import TelemedicineSession

User = get_user_model()


class TelemedicineSessionSerializer(serializers.ModelSerializer):
    branch = PublicIdRelatedField(queryset=Branch.objects.all())
    patient = PublicIdRelatedField(queryset=Patient.objects.all())
    provider = PublicIdRelatedField(queryset=User.objects.all())

    class Meta:
        model = TelemedicineSession
        fields = [
            "public_id", "branch", "patient", "provider", "scheduled_start", "scheduled_end",
            "status", "session_url", "session_token", "created_at", "updated_at",
        ]
        read_only_fields = ["public_id", "created_at", "updated_at"]
