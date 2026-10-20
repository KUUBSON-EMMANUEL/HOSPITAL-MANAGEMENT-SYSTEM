from rest_framework.routers import DefaultRouter

from .views import ImagingOrderViewSet

app_name = "radiology"

router = DefaultRouter()
router.register("orders", ImagingOrderViewSet, basename="imagingorder")

urlpatterns = router.urls
