from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.branches.models import Branch
from apps.core.serializers import PublicIdRelatedField
from apps.patients.models import Patient

from .models import TheatreBooking

User = get_user_model()


class TheatreBookingSerializer(serializers.ModelSerializer):
    branch = PublicIdRelatedField(queryset=Branch.objects.all())
    patient = PublicIdRelatedField(queryset=Patient.objects.all())
    surgeon = PublicIdRelatedField(queryset=User.objects.all())

    class Meta:
        model = TheatreBooking
        fields = [
            "public_id", "branch", "patient", "surgeon", "procedure_name",
            "scheduled_start", "scheduled_end", "status", "notes", "created_at", "updated_at",
        ]
        read_only_fields = ["public_id", "created_at", "updated_at"]
