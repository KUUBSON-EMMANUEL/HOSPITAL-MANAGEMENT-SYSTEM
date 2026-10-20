from apps.authentication.constants import ModuleCode
from apps.core.filters import build_filterset
from apps.core.permissions import ModulePermission
from apps.core.viewsets import BaseModelViewSet

from .models import Consultation
from .serializers import ConsultationSerializer


class ConsultationViewSet(BaseModelViewSet):
    queryset = Consultation.objects.select_related("branch", "patient", "provider", "appointment", "encounter").all()
    serializer_class = ConsultationSerializer
    permission_classes = [ModulePermission]
    module_code = ModuleCode.CONSULTATIONS
    filterset_class = build_filterset(Consultation, ["branch", "patient", "provider", "status"])
    ordering_fields = ["created_at"]
    search_fields = ["chief_complaint", "patient__first_name", "patient__last_name"]
