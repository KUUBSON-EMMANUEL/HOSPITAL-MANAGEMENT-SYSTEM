from apps.authentication.constants import ModuleCode
from apps.core.filters import build_filterset
from apps.core.permissions import ModulePermission
from apps.core.viewsets import BaseModelViewSet

from .models import TheatreBooking
from .serializers import TheatreBookingSerializer


class TheatreBookingViewSet(BaseModelViewSet):
    queryset = TheatreBooking.objects.select_related("branch", "patient", "surgeon").all()
    serializer_class = TheatreBookingSerializer
    permission_classes = [ModulePermission]
    module_code = ModuleCode.THEATRE
    filterset_class = build_filterset(TheatreBooking, ["branch", "patient", "surgeon", "status"])
    search_fields = ["procedure_name", "patient__first_name", "patient__last_name"]
    ordering_fields = ["scheduled_start"]
