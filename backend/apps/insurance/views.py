from apps.authentication.constants import ModuleCode
from apps.core.filters import build_filterset
from apps.core.permissions import ModulePermission
from apps.core.viewsets import BaseModelViewSet

from .models import InsurancePolicy
from .serializers import InsurancePolicySerializer


class InsurancePolicyViewSet(BaseModelViewSet):
    queryset = InsurancePolicy.objects.select_related("branch", "patient").all()
    serializer_class = InsurancePolicySerializer
    permission_classes = [ModulePermission]
    module_code = ModuleCode.INSURANCE
    filterset_class = build_filterset(InsurancePolicy, ["branch", "patient", "status", "provider_name"])
    search_fields = ["provider_name", "policy_number", "patient__first_name", "patient__last_name"]
    ordering_fields = ["valid_from", "valid_to", "created_at"]
