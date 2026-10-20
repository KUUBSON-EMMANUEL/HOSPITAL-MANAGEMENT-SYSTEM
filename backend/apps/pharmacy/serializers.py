from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.branches.models import Branch
from apps.core.serializers import PublicIdRelatedField
from apps.patients.models import Patient

from .models import Prescription, PrescriptionItem

User = get_user_model()


class PrescriptionSerializer(serializers.ModelSerializer):
    branch = PublicIdRelatedField(queryset=Branch.objects.all())
    patient = PublicIdRelatedField(queryset=Patient.objects.all())
    prescriber = PublicIdRelatedField(queryset=User.objects.all())

    class Meta:
        model = Prescription
        fields = [
            "public_id", "branch", "patient", "prescriber", "status", "notes",
            "created_at", "updated_at",
        ]
        read_only_fields = ["public_id", "created_at", "updated_at"]


class PrescriptionItemSerializer(serializers.ModelSerializer):
    prescription = PublicIdRelatedField(queryset=Prescription.objects.all())

    class Meta:
        model = PrescriptionItem
        fields = [
            "public_id", "prescription", "drug_name", "dosage", "frequency", "duration", "quantity",
            "created_at", "updated_at",
        ]
        read_only_fields = ["public_id", "created_at", "updated_at"]
