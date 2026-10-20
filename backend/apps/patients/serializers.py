from rest_framework import serializers

from apps.branches.models import Branch
from apps.core.serializers import PublicIdRelatedField

from .models import Patient, generate_patient_number


class PatientSerializer(serializers.ModelSerializer):
    branch = PublicIdRelatedField(queryset=Branch.objects.all())

    class Meta:
        model = Patient
        fields = [
            "public_id", "patient_number", "branch",
            "first_name", "last_name", "middle_name", "date_of_birth", "sex", "blood_type",
            "phone_number", "email", "address_line1", "address_line2", "city", "state_region", "country",
            "emergency_contact_name", "emergency_contact_phone", "emergency_contact_relationship",
            "allergies", "registration_date", "created_at", "updated_at",
        ]
        read_only_fields = ["public_id", "patient_number", "registration_date", "created_at", "updated_at"]

    def create(self, validated_data):
        validated_data["patient_number"] = generate_patient_number(validated_data["branch"])
        return super().create(validated_data)
