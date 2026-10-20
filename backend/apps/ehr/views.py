from apps.authentication.constants import ModuleCode
from apps.core.filters import build_filterset
from apps.core.permissions import ModulePermission
from apps.core.viewsets import BaseModelViewSet

from .models import Encounter, VitalSigns
from .serializers import EncounterSerializer, VitalSignsSerializer


class EncounterViewSet(BaseModelViewSet):
    queryset = Encounter.objects.select_related("branch", "patient", "appointment", "attending_provider").all()
    serializer_class = EncounterSerializer
    permission_classes = [ModulePermission]
    module_code = ModuleCode.EHR
    filterset_class = build_filterset(Encounter, ["branch", "patient", "status", "encounter_type"])
    ordering_fields = ["started_at"]
    search_fields = ["chief_complaint", "patient__first_name", "patient__last_name"]


class VitalSignsViewSet(BaseModelViewSet):
    queryset = VitalSigns.objects.select_related("branch", "patient", "encounter", "recorded_by").all()
    serializer_class = VitalSignsSerializer
    permission_classes = [ModulePermission]
    module_code = ModuleCode.EHR
    filterset_class = build_filterset(VitalSigns, ["branch", "patient", "encounter"])
    ordering_fields = ["recorded_at"]
