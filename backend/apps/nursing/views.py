from apps.authentication.constants import ModuleCode
from apps.core.filters import build_filterset
from apps.core.permissions import ModulePermission
from apps.core.viewsets import BaseModelViewSet

from .models import NursingNote
from .serializers import NursingNoteSerializer


class NursingNoteViewSet(BaseModelViewSet):
    queryset = NursingNote.objects.select_related("branch", "patient", "encounter", "nurse").all()
    serializer_class = NursingNoteSerializer
    permission_classes = [ModulePermission]
    module_code = ModuleCode.NURSING
    filterset_class = build_filterset(NursingNote, ["branch", "patient", "encounter", "nurse", "shift"])
    search_fields = ["note", "patient__first_name", "patient__last_name"]
    ordering_fields = ["created_at"]
