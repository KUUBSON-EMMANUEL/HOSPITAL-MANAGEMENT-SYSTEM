from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.branches.models import Branch
from apps.core.serializers import PublicIdRelatedField

from .models import InventoryItem, StockMovement

User = get_user_model()


class InventoryItemSerializer(serializers.ModelSerializer):
    branch = PublicIdRelatedField(queryset=Branch.objects.all())

    class Meta:
        model = InventoryItem
        fields = [
            "public_id", "branch", "name", "sku", "unit", "quantity_on_hand", "reorder_level",
            "created_at", "updated_at",
        ]
        read_only_fields = ["public_id", "created_at", "updated_at"]


class StockMovementSerializer(serializers.ModelSerializer):
    item = PublicIdRelatedField(queryset=InventoryItem.objects.all())
    recorded_by = PublicIdRelatedField(queryset=User.objects.all())

    class Meta:
        model = StockMovement
        fields = [
            "public_id", "item", "movement_type", "quantity", "reason", "recorded_by",
            "created_at", "updated_at",
        ]
        read_only_fields = ["public_id", "created_at", "updated_at"]
