from apps.authentication.constants import ModuleCode
from apps.core.filters import build_filterset
from apps.core.permissions import ModulePermission
from apps.core.viewsets import BaseModelViewSet

from .models import SavedReport
from .serializers import SavedReportSerializer


class SavedReportViewSet(BaseModelViewSet):
    queryset = SavedReport.objects.select_related("branch", "generated_by").all()
    serializer_class = SavedReportSerializer
    permission_classes = [ModulePermission]
    module_code = ModuleCode.REPORTS
    filterset_class = build_filterset(SavedReport, ["branch", "report_type", "generated_by"])
    search_fields = ["name", "report_type"]
    ordering_fields = ["created_at", "generated_at"]
