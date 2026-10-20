from rest_framework.routers import DefaultRouter

from .views import TheatreBookingViewSet

app_name = "theatre"

router = DefaultRouter()
router.register("bookings", TheatreBookingViewSet, basename="theatrebooking")

urlpatterns = router.urls
