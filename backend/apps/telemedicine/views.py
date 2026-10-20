from apps.authentication.constants import ModuleCode
from apps.core.filters import build_filterset
from apps.core.permissions import ModulePermission
from apps.core.viewsets import BaseModelViewSet

from .models import TelemedicineSession
from .serializers import TelemedicineSessionSerializer


class TelemedicineSessionViewSet(BaseModelViewSet):
    queryset = TelemedicineSession.objects.select_related("branch", "patient", "provider").all()
    serializer_class = TelemedicineSessionSerializer
    permission_classes = [ModulePermission]
    module_code = ModuleCode.TELEMEDICINE
    filterset_class = build_filterset(TelemedicineSession, ["branch", "patient", "provider", "status"])
    search_fields = ["patient__first_name", "patient__last_name"]
    ordering_fields = ["scheduled_start"]
