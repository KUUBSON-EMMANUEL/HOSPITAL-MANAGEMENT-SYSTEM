from apps.authentication.constants import ModuleCode
from apps.core.filters import build_filterset
from apps.core.permissions import ModulePermission
from apps.core.viewsets import BaseModelViewSet

from .models import InventoryItem, StockMovement
from .serializers import InventoryItemSerializer, StockMovementSerializer


class InventoryItemViewSet(BaseModelViewSet):
    queryset = InventoryItem.objects.select_related("branch").all()
    serializer_class = InventoryItemSerializer
    permission_classes = [ModulePermission]
    module_code = ModuleCode.INVENTORY
    filterset_class = build_filterset(InventoryItem, ["branch"])
    search_fields = ["name", "sku"]
    ordering_fields = ["name", "quantity_on_hand", "created_at"]


class StockMovementViewSet(BaseModelViewSet):
    queryset = StockMovement.objects.select_related("item", "recorded_by").all()
    serializer_class = StockMovementSerializer
    permission_classes = [ModulePermission]
    module_code = ModuleCode.INVENTORY
    filterset_class = build_filterset(StockMovement, ["item", "movement_type", "recorded_by"])
    search_fields = ["reason", "item__name", "item__sku"]
    ordering_fields = ["created_at"]
