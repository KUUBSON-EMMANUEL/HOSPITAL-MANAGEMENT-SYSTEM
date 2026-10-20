from rest_framework.routers import DefaultRouter

from .views import SavedReportViewSet

app_name = "reports"

router = DefaultRouter()
router.register("", SavedReportViewSet, basename="savedreport")

urlpatterns = router.urls
