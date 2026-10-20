from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.branches.models import Branch
from apps.core.serializers import PublicIdRelatedField
from apps.patients.models import Patient

from .models import MaternityRecord

User = get_user_model()


class MaternityRecordSerializer(serializers.ModelSerializer):
    branch = PublicIdRelatedField(queryset=Branch.objects.all())
    patient = PublicIdRelatedField(queryset=Patient.objects.all())
    attending_provider = PublicIdRelatedField(queryset=User.objects.all())

    class Meta:
        model = MaternityRecord
        fields = [
            "public_id", "branch", "patient", "attending_provider", "expected_delivery_date",
            "status", "notes", "created_at", "updated_at",
        ]
        read_only_fields = ["public_id", "created_at", "updated_at"]
