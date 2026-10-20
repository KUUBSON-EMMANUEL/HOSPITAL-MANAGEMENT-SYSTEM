from rest_framework import serializers

from apps.branches.models import Branch
from apps.core.serializers import PublicIdRelatedField
from apps.patients.models import Patient

from .models import Bed


class BedSerializer(serializers.ModelSerializer):
    branch = PublicIdRelatedField(queryset=Branch.objects.all())
    current_patient = PublicIdRelatedField(queryset=Patient.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Bed
        fields = [
            "public_id", "branch", "ward_name", "bed_number", "bed_type", "status",
            "current_patient", "created_at", "updated_at",
        ]
        read_only_fields = ["public_id", "created_at", "updated_at"]
