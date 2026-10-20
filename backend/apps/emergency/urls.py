from rest_framework.routers import DefaultRouter

from .views import EmergencyCaseViewSet

app_name = "emergency"

router = DefaultRouter()
router.register("cases", EmergencyCaseViewSet, basename="emergencycase")

urlpatterns = router.urls
