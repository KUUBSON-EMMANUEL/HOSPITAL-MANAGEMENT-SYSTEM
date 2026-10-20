from apps.authentication.constants import ModuleCode
from apps.core.filters import build_filterset
from apps.core.permissions import ModulePermission
from apps.core.viewsets import BaseModelViewSet

from .models import EmergencyCase
from .serializers import EmergencyCaseSerializer


class EmergencyCaseViewSet(BaseModelViewSet):
    queryset = EmergencyCase.objects.select_related("branch", "patient", "attending_provider").all()
    serializer_class = EmergencyCaseSerializer
    permission_classes = [ModulePermission]
    module_code = ModuleCode.EMERGENCY
    filterset_class = build_filterset(EmergencyCase, ["branch", "patient", "triage_level", "status", "attending_provider"])
    search_fields = ["chief_complaint", "patient__first_name", "patient__last_name"]
    ordering_fields = ["arrival_time"]
