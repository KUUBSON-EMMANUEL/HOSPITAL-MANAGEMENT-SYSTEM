from apps.authentication.constants import ModuleCode
from apps.core.filters import build_filterset
from apps.core.permissions import ModulePermission
from apps.core.viewsets import BaseModelViewSet

from .models import StaffProfile
from .serializers import StaffProfileSerializer


class StaffProfileViewSet(BaseModelViewSet):
    queryset = StaffProfile.objects.select_related("user").all()
    serializer_class = StaffProfileSerializer
    permission_classes = [ModulePermission]
    module_code = ModuleCode.STAFF
    filterset_class = build_filterset(StaffProfile, ["department", "designation", "employment_status"])
    search_fields = ["user__email", "user__first_name", "user__last_name", "department", "designation"]
    ordering_fields = ["hire_date", "created_at"]
