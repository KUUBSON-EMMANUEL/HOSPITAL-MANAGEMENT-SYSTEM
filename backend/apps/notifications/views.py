from apps.authentication.constants import ModuleCode
from apps.core.filters import build_filterset
from apps.core.permissions import ModulePermission
from apps.core.viewsets import BaseModelViewSet

from .models import Notification
from .serializers import NotificationSerializer


class NotificationViewSet(BaseModelViewSet):
    queryset = Notification.objects.select_related("recipient").all()
    serializer_class = NotificationSerializer
    permission_classes = [ModulePermission]
    module_code = ModuleCode.NOTIFICATIONS
    filterset_class = build_filterset(Notification, ["recipient", "channel", "status"])
    search_fields = ["title", "body"]
    ordering_fields = ["created_at", "sent_at"]
