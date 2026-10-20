from apps.authentication.constants import ModuleCode
from apps.core.filters import build_filterset
from apps.core.permissions import ModulePermission
from apps.core.viewsets import BaseModelViewSet

from .models import Invoice, InvoiceLineItem
from .serializers import InvoiceLineItemSerializer, InvoiceSerializer


class InvoiceViewSet(BaseModelViewSet):
    queryset = Invoice.objects.select_related("branch", "patient").all()
    serializer_class = InvoiceSerializer
    permission_classes = [ModulePermission]
    module_code = ModuleCode.BILLING
    filterset_class = build_filterset(Invoice, ["branch", "patient", "status"])
    search_fields = ["invoice_number", "patient__first_name", "patient__last_name"]
    ordering_fields = ["created_at", "due_date", "total_amount"]


class InvoiceLineItemViewSet(BaseModelViewSet):
    queryset = InvoiceLineItem.objects.select_related("invoice").all()
    serializer_class = InvoiceLineItemSerializer
    permission_classes = [ModulePermission]
    module_code = ModuleCode.BILLING
    filterset_class = build_filterset(InvoiceLineItem, ["invoice", "module_reference"])
    search_fields = ["description"]
    ordering_fields = ["created_at"]
