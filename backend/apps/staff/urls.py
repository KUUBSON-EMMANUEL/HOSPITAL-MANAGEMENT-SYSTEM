from rest_framework.routers import DefaultRouter

from .views import StaffProfileViewSet

app_name = "staff"

router = DefaultRouter()
router.register("profiles", StaffProfileViewSet, basename="staffprofile")

urlpatterns = router.urls
