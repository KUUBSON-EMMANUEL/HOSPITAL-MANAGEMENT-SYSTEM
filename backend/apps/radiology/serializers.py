from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.branches.models import Branch
from apps.core.serializers import PublicIdRelatedField
from apps.patients.models import Patient

from .models import ImagingOrder

User = get_user_model()


class ImagingOrderSerializer(serializers.ModelSerializer):
    branch = PublicIdRelatedField(queryset=Branch.objects.all())
    patient = PublicIdRelatedField(queryset=Patient.objects.all())
    ordering_provider = PublicIdRelatedField(queryset=User.objects.all())

    class Meta:
        model = ImagingOrder
        fields = [
            "public_id", "branch", "patient", "ordering_provider", "modality", "status",
            "ordered_at", "findings", "report", "completed_at", "created_at", "updated_at",
        ]
        read_only_fields = ["public_id", "ordered_at", "created_at", "updated_at"]
