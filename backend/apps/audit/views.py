from django_filters import rest_framework as django_filters
from rest_framework import filters, viewsets

from apps.authentication.constants import ModuleCode
from apps.core.permissions import ModulePermission

from .models import AuditLog
from .serializers import AuditLogSerializer


class AuditLogFilterSet(django_filters.FilterSet):
    created_after = django_filters.DateTimeFilter(field_name="created_at", lookup_expr="gte")
    created_before = django_filters.DateTimeFilter(field_name="created_at", lookup_expr="lte")
    # actor/branch filter by public_id, not the internal pk -- matches every
    # other list endpoint's FK filtering (see apps.core.filters.build_filterset).
    actor = django_filters.CharFilter(field_name="actor__public_id")
    branch = django_filters.CharFilter(field_name="branch__public_id")

    class Meta:
        model = AuditLog
        fields = ["action", "severity"]


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only compliance trail -- gated to roles holding an
    AUDIT/view Permission (e.g. COMPLIANCE_OFFICER); super-admins bypass
    via ModulePermission's is_superuser short-circuit."""

    queryset = AuditLog.objects.select_related("actor", "branch").all()
    serializer_class = AuditLogSerializer
    lookup_field = "public_id"
    permission_classes = [ModulePermission]
    module_code = ModuleCode.AUDIT
    filter_backends = [django_filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = AuditLogFilterSet
    search_fields = ["target_repr", "request_path"]
    ordering_fields = ["created_at", "status_code", "duration_ms"]
    ordering = ["-created_at"]
