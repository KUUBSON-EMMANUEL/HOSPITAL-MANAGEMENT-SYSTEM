from rest_framework.routers import DefaultRouter

from .views import TelemedicineSessionViewSet

app_name = "telemedicine"

router = DefaultRouter()
router.register("sessions", TelemedicineSessionViewSet, basename="telemedicinesession")

urlpatterns = router.urls
