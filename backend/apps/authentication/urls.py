from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

app_name = "authentication"

router = DefaultRouter()
router.register("users", views.UserDirectoryViewSet, basename="user-directory")

urlpatterns = [
    path("", include(router.urls)),
    path("login/", views.LoginView.as_view(), name="login"),
    path("mfa/verify/", views.MFAVerifyView.as_view(), name="mfa-verify"),
    path("refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("me/", views.MeView.as_view(), name="me"),
    path("change-password/", views.ChangePasswordView.as_view(), name="change-password"),
    path("mfa/enable/", views.MFAEnableView.as_view(), name="mfa-enable"),
    path("mfa/verify-setup/", views.MFAVerifySetupView.as_view(), name="mfa-verify-setup"),
    path("mfa/disable/", views.MFADisableView.as_view(), name="mfa-disable"),
]
