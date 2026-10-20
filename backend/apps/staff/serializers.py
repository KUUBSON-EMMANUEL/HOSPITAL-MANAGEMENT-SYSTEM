from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.core.serializers import PublicIdRelatedField

from .models import StaffProfile

User = get_user_model()


class StaffProfileSerializer(serializers.ModelSerializer):
    user = PublicIdRelatedField(queryset=User.objects.all())

    class Meta:
        model = StaffProfile
        fields = [
            "public_id", "user", "department", "designation", "hire_date", "employment_status",
            "created_at", "updated_at",
        ]
        read_only_fields = ["public_id", "created_at", "updated_at"]
