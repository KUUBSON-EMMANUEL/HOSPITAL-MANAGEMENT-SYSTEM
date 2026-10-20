from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.core.serializers import PublicIdRelatedField

from .models import Message

User = get_user_model()


class MessageSerializer(serializers.ModelSerializer):
    sender = PublicIdRelatedField(queryset=User.objects.all())
    recipient = PublicIdRelatedField(queryset=User.objects.all())

    class Meta:
        model = Message
        fields = [
            "public_id", "sender", "recipient", "body", "read_at", "created_at", "updated_at",
        ]
        read_only_fields = ["public_id", "created_at", "updated_at"]
