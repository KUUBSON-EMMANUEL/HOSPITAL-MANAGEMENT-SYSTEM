from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.appointments.models import Appointment
from apps.branches.models import Branch
from apps.core.serializers import PublicIdRelatedField
from apps.patients.models import Patient

from .models import Encounter, VitalSigns

User = get_user_model()


class EncounterSerializer(serializers.ModelSerializer):
    branch = PublicIdRelatedField(queryset=Branch.objects.all())
    patient = PublicIdRelatedField(queryset=Patient.objects.all())
    appointment = PublicIdRelatedField(queryset=Appointment.objects.all(), required=False, allow_null=True)
    attending_provider = PublicIdRelatedField(queryset=User.objects.all())

    class Meta:
        model = Encounter
        fields = [
            "public_id", "branch", "patient", "appointment", "attending_provider",
            "encounter_type", "status", "started_at", "ended_at", "chief_complaint",
            "created_at", "updated_at",
        ]
        read_only_fields = ["public_id", "started_at", "created_at", "updated_at"]


class VitalSignsSerializer(serializers.ModelSerializer):
    branch = PublicIdRelatedField(queryset=Branch.objects.all())
    patient = PublicIdRelatedField(queryset=Patient.objects.all())
    encounter = PublicIdRelatedField(queryset=Encounter.objects.all(), required=False, allow_null=True)
    recorded_by = PublicIdRelatedField(queryset=User.objects.all())

    class Meta:
        model = VitalSigns
        fields = [
            "public_id", "branch", "patient", "encounter", "recorded_by", "recorded_at",
            "temperature_celsius", "pulse_bpm", "respiratory_rate", "systolic_bp", "diastolic_bp",
            "spo2_percent", "weight_kg", "height_cm", "created_at", "updated_at",
        ]
        read_only_fields = ["public_id", "recorded_at", "created_at", "updated_at"]
