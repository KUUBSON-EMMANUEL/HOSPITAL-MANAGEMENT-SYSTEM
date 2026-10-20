from apps.authentication.constants import ModuleCode
from apps.core.filters import build_filterset
from apps.core.permissions import ModulePermission
from apps.core.viewsets import BaseModelViewSet

from .models import MaternityRecord
from .serializers import MaternityRecordSerializer


class MaternityRecordViewSet(BaseModelViewSet):
    queryset = MaternityRecord.objects.select_related("branch", "patient", "attending_provider").all()
    serializer_class = MaternityRecordSerializer
    permission_classes = [ModulePermission]
    module_code = ModuleCode.MATERNITY
    filterset_class = build_filterset(MaternityRecord, ["branch", "patient", "attending_provider", "status"])
    search_fields = ["patient__first_name", "patient__last_name", "notes"]
    ordering_fields = ["expected_delivery_date", "created_at"]
