from apps.authentication.constants import ModuleCode
from apps.core.filters import build_filterset
from apps.core.permissions import ModulePermission
from apps.core.viewsets import BaseModelViewSet

from .models import Prescription, PrescriptionItem
from .serializers import PrescriptionItemSerializer, PrescriptionSerializer


class PrescriptionViewSet(BaseModelViewSet):
    queryset = Prescription.objects.select_related("branch", "patient", "prescriber").all()
    serializer_class = PrescriptionSerializer
    permission_classes = [ModulePermission]
    module_code = ModuleCode.PHARMACY
    filterset_class = build_filterset(Prescription, ["branch", "patient", "prescriber", "status"])
    search_fields = ["patient__first_name", "patient__last_name", "notes"]
    ordering_fields = ["created_at"]


class PrescriptionItemViewSet(BaseModelViewSet):
    queryset = PrescriptionItem.objects.select_related("prescription").all()
    serializer_class = PrescriptionItemSerializer
    permission_classes = [ModulePermission]
    module_code = ModuleCode.PHARMACY
    filterset_class = build_filterset(PrescriptionItem, ["prescription"])
    search_fields = ["drug_name"]
    ordering_fields = ["created_at"]
