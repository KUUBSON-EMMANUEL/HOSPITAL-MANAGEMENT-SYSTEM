from apps.authentication.constants import ModuleCode
from apps.core.filters import build_filterset
from apps.core.permissions import ModulePermission
from apps.core.viewsets import BaseModelViewSet

from .models import Bed
from .serializers import BedSerializer


class BedViewSet(BaseModelViewSet):
    queryset = Bed.objects.select_related("branch", "current_patient").all()
    serializer_class = BedSerializer
    permission_classes = [ModulePermission]
    module_code = ModuleCode.WARDS
    filterset_class = build_filterset(Bed, ["branch", "ward_name", "bed_type", "status", "current_patient"])
    search_fields = ["ward_name", "bed_number"]
    ordering_fields = ["ward_name", "bed_number", "created_at"]
