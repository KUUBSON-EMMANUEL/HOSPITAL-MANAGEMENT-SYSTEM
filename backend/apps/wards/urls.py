from rest_framework.routers import DefaultRouter

from .views import BedViewSet

app_name = "wards"

router = DefaultRouter()
router.register("beds", BedViewSet, basename="bed")

urlpatterns = router.urls
