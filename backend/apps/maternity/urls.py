from rest_framework.routers import DefaultRouter

from .views import MaternityRecordViewSet

app_name = "maternity"

router = DefaultRouter()
router.register("records", MaternityRecordViewSet, basename="maternityrecord")

urlpatterns = router.urls
