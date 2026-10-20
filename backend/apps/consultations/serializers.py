from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.appointments.models import Appointment
from apps.branches.models import Branch
from apps.core.serializers import PublicIdRelatedField
from apps.ehr.models import Encounter
from apps.patients.models import Patient

from .models import Consultation

User = get_user_model()


class ConsultationSerializer(serializers.ModelSerializer):
    branch = PublicIdRelatedField(queryset=Branch.objects.all())
    patient = PublicIdRelatedField(queryset=Patient.objects.all())
    provider = PublicIdRelatedField(queryset=User.objects.all())
    appointment = PublicIdRelatedField(queryset=Appointment.objects.all(), required=False, allow_null=True)
    encounter = PublicIdRelatedField(queryset=Encounter.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Consultation
        fields = [
            "public_id", "branch", "patient", "provider", "appointment", "encounter",
            "chief_complaint", "subjective", "objective", "assessment", "plan", "diagnosis", "status",
            "created_at", "updated_at",
        ]
        read_only_fields = ["public_id", "created_at", "updated_at"]
