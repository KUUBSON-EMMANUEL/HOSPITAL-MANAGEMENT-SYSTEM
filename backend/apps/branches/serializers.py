from rest_framework import serializers

from .models import Branch


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = [
            "public_id", "code", "name", "is_main_branch", "is_active",
            "address_line1", "address_line2", "city", "state_region", "country", "postal_code",
            "phone_number", "email", "timezone", "license_number", "bed_capacity",
            "created_at", "updated_at",
        ]
        read_only_fields = ["public_id", "created_at", "updated_at"]
