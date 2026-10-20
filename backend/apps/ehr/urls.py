from rest_framework.routers import DefaultRouter

from .views import EncounterViewSet, VitalSignsViewSet

app_name = "ehr"

router = DefaultRouter()
router.register("encounters", EncounterViewSet, basename="encounter")
router.register("vitals", VitalSignsViewSet, basename="vitalsigns")

urlpatterns = router.urls
