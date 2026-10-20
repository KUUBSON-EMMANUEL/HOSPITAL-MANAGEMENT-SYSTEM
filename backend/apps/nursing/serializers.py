from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.branches.models import Branch
from apps.core.serializers import PublicIdRelatedField
from apps.ehr.models import Encounter
from apps.patients.models import Patient

from .models import NursingNote

User = get_user_model()


class NursingNoteSerializer(serializers.ModelSerializer):
    branch = PublicIdRelatedField(queryset=Branch.objects.all())
    patient = PublicIdRelatedField(queryset=Patient.objects.all())
    encounter = PublicIdRelatedField(queryset=Encounter.objects.all(), required=False, allow_null=True)
    nurse = PublicIdRelatedField(queryset=User.objects.all())

    class Meta:
        model = NursingNote
        fields = [
            "public_id", "branch", "patient", "encounter", "nurse", "note", "shift",
            "created_at", "updated_at",
        ]
        read_only_fields = ["public_id", "created_at", "updated_at"]
