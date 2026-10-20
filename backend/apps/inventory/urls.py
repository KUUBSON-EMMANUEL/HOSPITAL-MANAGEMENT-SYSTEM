from rest_framework.routers import DefaultRouter

from .views import InventoryItemViewSet, StockMovementViewSet

app_name = "inventory"

router = DefaultRouter()
router.register("items", InventoryItemViewSet, basename="inventoryitem")
router.register("movements", StockMovementViewSet, basename="stockmovement")

urlpatterns = router.urls
