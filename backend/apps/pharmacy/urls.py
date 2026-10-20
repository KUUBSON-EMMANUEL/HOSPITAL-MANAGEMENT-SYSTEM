from rest_framework.routers import DefaultRouter

from .views import PrescriptionItemViewSet, PrescriptionViewSet

app_name = "pharmacy"

router = DefaultRouter()
router.register("prescriptions", PrescriptionViewSet, basename="prescription")
router.register("items", PrescriptionItemViewSet, basename="prescriptionitem")

urlpatterns = router.urls
