from apps.authentication.constants import ModuleCode
from apps.core.filters import build_filterset
from apps.core.permissions import ModulePermission
from apps.core.viewsets import BaseModelViewSet

from .models import Message
from .serializers import MessageSerializer


class MessageViewSet(BaseModelViewSet):
    queryset = Message.objects.select_related("sender", "recipient").all()
    serializer_class = MessageSerializer
    permission_classes = [ModulePermission]
    module_code = ModuleCode.MESSAGING
    filterset_class = build_filterset(Message, ["sender", "recipient"])
    search_fields = ["body"]
    ordering_fields = ["created_at"]
