from rest_framework.routers import DefaultRouter

from .views import InsurancePolicyViewSet

app_name = "insurance"

router = DefaultRouter()
router.register("policies", InsurancePolicyViewSet, basename="insurancepolicy")

urlpatterns = router.urls
