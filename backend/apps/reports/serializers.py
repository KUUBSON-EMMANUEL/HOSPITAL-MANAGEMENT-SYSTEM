from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.branches.models import Branch
from apps.core.serializers import PublicIdRelatedField

from .models import SavedReport

User = get_user_model()


class SavedReportSerializer(serializers.ModelSerializer):
    branch = PublicIdRelatedField(queryset=Branch.objects.all())
    generated_by = PublicIdRelatedField(queryset=User.objects.all(), required=False, allow_null=True)

    class Meta:
        model = SavedReport
        fields = [
            "public_id", "branch", "name", "report_type", "parameters", "generated_at",
            "generated_by", "output_file", "created_at", "updated_at",
        ]
        read_only_fields = ["public_id", "created_at", "updated_at"]
