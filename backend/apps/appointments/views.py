from apps.authentication.constants import ModuleCode
from apps.core.filters import build_filterset
from apps.core.permissions import ModulePermission
from apps.core.viewsets import BaseModelViewSet

from .models import Appointment
from .serializers import AppointmentSerializer


class AppointmentViewSet(BaseModelViewSet):
    queryset = Appointment.objects.select_related("branch", "patient", "provider").all()
    serializer_class = AppointmentSerializer
    permission_classes = [ModulePermission]
    module_code = ModuleCode.APPOINTMENTS
    filterset_class = build_filterset(Appointment, ["branch", "patient", "provider", "status", "appointment_type"])
    ordering_fields = ["scheduled_start"]
    search_fields = ["reason", "patient__first_name", "patient__last_name"]
