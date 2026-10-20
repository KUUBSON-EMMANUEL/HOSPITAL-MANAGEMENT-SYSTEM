from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

api_v1_patterns = [
    path("auth/", include("apps.authentication.urls")),
    path("patients/", include("apps.patients.urls")),
    path("ehr/", include("apps.ehr.urls")),
    path("consultations/", include("apps.consultations.urls")),
    path("nursing/", include("apps.nursing.urls")),
    path("laboratory/", include("apps.laboratory.urls")),
    path("radiology/", include("apps.radiology.urls")),
    path("pharmacy/", include("apps.pharmacy.urls")),
    path("inventory/", include("apps.inventory.urls")),
    path("billing/", include("apps.billing.urls")),
    path("insurance/", include("apps.insurance.urls")),
    path("appointments/", include("apps.appointments.urls")),
    path("wards/", include("apps.wards.urls")),
    path("emergency/", include("apps.emergency.urls")),
    path("theatre/", include("apps.theatre.urls")),
    path("maternity/", include("apps.maternity.urls")),
    path("telemedicine/", include("apps.telemedicine.urls")),
    path("staff/", include("apps.staff.urls")),
    path("reports/", include("apps.reports.urls")),
    path("audit/", include("apps.audit.urls")),
    path("notifications/", include("apps.notifications.urls")),
    path("messaging/", include("apps.messaging.urls")),
    path("branches/", include("apps.branches.urls")),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(api_v1_patterns)),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
