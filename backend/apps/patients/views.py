from apps.authentication.constants import ModuleCode
from apps.core.filters import build_filterset
from apps.core.permissions import ModulePermission
from apps.core.viewsets import BaseModelViewSet

from .models import Patient
from .serializers import PatientSerializer


class PatientViewSet(BaseModelViewSet):
    """Uses the DRF-default filter backends (DjangoFilterBackend + Search +
    Ordering, see REST_FRAMEWORK['DEFAULT_FILTER_BACKENDS']) rather than
    overriding filter_backends, so filterset_class keeps working."""

    queryset = Patient.objects.select_related("branch").all()
    serializer_class = PatientSerializer
    permission_classes = [ModulePermission]
    module_code = ModuleCode.PATIENTS
    search_fields = ["patient_number", "first_name", "last_name", "phone_number", "email"]
    ordering_fields = ["registration_date", "last_name"]
    filterset_class = build_filterset(Patient, ["branch", "sex", "blood_type"])
