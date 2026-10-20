from apps.authentication.constants import ModuleCode
from apps.core.filters import build_filterset
from apps.core.permissions import ModulePermission
from apps.core.viewsets import BaseModelViewSet

from .models import LabOrder
from .serializers import LabOrderSerializer


class LabOrderViewSet(BaseModelViewSet):
    queryset = LabOrder.objects.select_related("branch", "patient", "ordering_provider").all()
    serializer_class = LabOrderSerializer
    permission_classes = [ModulePermission]
    module_code = ModuleCode.LABORATORY
    filterset_class = build_filterset(LabOrder, ["branch", "patient", "ordering_provider", "status"])
    search_fields = ["test_name", "patient__first_name", "patient__last_name"]
    ordering_fields = ["ordered_at", "completed_at"]
