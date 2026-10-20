from rest_framework.routers import DefaultRouter

from .views import LabOrderViewSet

app_name = "laboratory"

router = DefaultRouter()
router.register("orders", LabOrderViewSet, basename="laborder")

urlpatterns = router.urls
