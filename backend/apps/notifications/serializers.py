from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.core.serializers import PublicIdRelatedField

from .models import Notification

User = get_user_model()


class NotificationSerializer(serializers.ModelSerializer):
    recipient = PublicIdRelatedField(queryset=User.objects.all())

    class Meta:
        model = Notification
        fields = [
            "public_id", "recipient", "title", "body", "channel", "status", "sent_at",
            "created_at", "updated_at",
        ]
        read_only_fields = ["public_id", "created_at", "updated_at"]
