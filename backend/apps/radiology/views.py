from apps.authentication.constants import ModuleCode
from apps.core.filters import build_filterset
from apps.core.permissions import ModulePermission
from apps.core.viewsets import BaseModelViewSet

from .models import ImagingOrder
from .serializers import ImagingOrderSerializer


class ImagingOrderViewSet(BaseModelViewSet):
    queryset = ImagingOrder.objects.select_related("branch", "patient", "ordering_provider").all()
    serializer_class = ImagingOrderSerializer
    permission_classes = [ModulePermission]
    module_code = ModuleCode.RADIOLOGY
    filterset_class = build_filterset(ImagingOrder, ["branch", "patient", "ordering_provider", "modality", "status"])
    search_fields = ["patient__first_name", "patient__last_name", "findings"]
    ordering_fields = ["ordered_at", "completed_at"]
