from rest_framework.routers import DefaultRouter

from .views import NursingNoteViewSet

app_name = "nursing"

router = DefaultRouter()
router.register("notes", NursingNoteViewSet, basename="nursingnote")

urlpatterns = router.urls
