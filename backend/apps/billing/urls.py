from rest_framework.routers import DefaultRouter

from .views import InvoiceLineItemViewSet, InvoiceViewSet

app_name = "billing"

router = DefaultRouter()
router.register("invoices", InvoiceViewSet, basename="invoice")
router.register("line-items", InvoiceLineItemViewSet, basename="invoicelineitem")

urlpatterns = router.urls
