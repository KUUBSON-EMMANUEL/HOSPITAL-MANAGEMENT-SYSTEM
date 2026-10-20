from rest_framework import serializers

from apps.branches.models import Branch
from apps.core.serializers import PublicIdRelatedField
from apps.patients.models import Patient

from .models import InsurancePolicy


class InsurancePolicySerializer(serializers.ModelSerializer):
    branch = PublicIdRelatedField(queryset=Branch.objects.all())
    patient = PublicIdRelatedField(queryset=Patient.objects.all())

    class Meta:
        model = InsurancePolicy
        fields = [
            "public_id", "branch", "patient", "provider_name", "policy_number", "coverage_type",
            "valid_from", "valid_to", "status", "created_at", "updated_at",
        ]
        read_only_fields = ["public_id", "created_at", "updated_at"]
