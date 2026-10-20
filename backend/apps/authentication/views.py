import pyotp
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from apps.audit.models import AuditAction, AuditLog
from apps.core.utils import get_client_ip

from .serializers import (
    ChangePasswordSerializer,
    CustomTokenObtainPairSerializer,
    LoginSerializer,
    MFADisableSerializer,
    MFAVerifySerializer,
    MFAVerifySetupSerializer,
    UserDirectorySerializer,
    UserProfileSerializer,
)
from .tokens import MFAChallengeToken

User = get_user_model()


def _issue_tokens(user):
    refresh = CustomTokenObtainPairSerializer.get_token(user)
    return {"access": str(refresh.access_token), "refresh": str(refresh)}


def _log(request, user, action, **metadata):
    AuditLog.objects.create(
        actor=user,
        actor_email_snapshot=user.email if user else "",
        branch=getattr(user, "branch", None) if user else None,
        action=action,
        ip_address=get_client_ip(request),
        user_agent=request.META.get("HTTP_USER_AGENT", "")[:500],
        request_method=request.method,
        request_path=request.path[:500],
        metadata=metadata,
    )


class LoginView(APIView):
    permission_classes = [AllowAny]
    throttle_scope = "auth"

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        user = authenticate(request, username=email, password=password)
        if user is None:
            _log(request, None, AuditAction.LOGIN_FAILED, email=email)
            raise AuthenticationFailed("Invalid email or password.")
        if not user.is_active:
            raise AuthenticationFailed("This account is inactive.")

        if user.mfa_enabled:
            challenge = MFAChallengeToken.for_user(user)
            _log(request, user, AuditAction.MFA_CHALLENGE_SENT)
            return Response({"mfa_required": True, "challenge_token": str(challenge)})

        _log(request, user, AuditAction.LOGIN_SUCCESS)
        return Response(_issue_tokens(user))


class MFAVerifyView(APIView):
    permission_classes = [AllowAny]
    throttle_scope = "otp"

    def post(self, request):
        serializer = MFAVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            token = MFAChallengeToken(serializer.validated_data["challenge_token"])
        except TokenError as exc:
            raise AuthenticationFailed("Invalid or expired challenge token.") from exc

        user = User.objects.filter(id=token["user_id"], is_active=True).first()
        if user is None or not user.mfa_enabled:
            raise AuthenticationFailed("Invalid challenge.")

        totp = pyotp.TOTP(user.mfa_secret)
        if not totp.verify(serializer.validated_data["otp_code"], valid_window=1):
            _log(request, user, AuditAction.MFA_FAILED)
            raise AuthenticationFailed("Invalid verification code.")

        _log(request, user, AuditAction.MFA_VERIFIED)
        return Response(_issue_tokens(user))


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh = request.data.get("refresh")
        if refresh:
            try:
                RefreshToken(refresh).blacklist()
            except TokenError:
                pass
        _log(request, request.user, AuditAction.LOGOUT)
        return Response(status=204)


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserProfileSerializer(request.user).data)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = request.user
        if not user.check_password(serializer.validated_data["old_password"]):
            raise ValidationError({"old_password": "Incorrect password."})
        user.set_password(serializer.validated_data["new_password"])
        user.must_change_password = False
        user.password_changed_at = timezone.now()
        user.save(update_fields=["password", "must_change_password", "password_changed_at"])
        _log(request, user, AuditAction.PASSWORD_CHANGED)
        return Response(status=204)


class MFAEnableView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        secret = pyotp.random_base32()
        user.mfa_secret = secret
        user.save(update_fields=["mfa_secret"])
        uri = pyotp.totp.TOTP(secret).provisioning_uri(name=user.email, issuer_name=settings.HMS_MFA_ISSUER_NAME)
        return Response({"secret": secret, "provisioning_uri": uri})


class MFAVerifySetupView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_scope = "otp"

    def post(self, request):
        serializer = MFAVerifySetupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        if not user.mfa_secret:
            raise ValidationError("MFA setup has not been started. Call mfa/enable/ first.")

        totp = pyotp.TOTP(user.mfa_secret)
        if not totp.verify(serializer.validated_data["otp_code"], valid_window=1):
            raise ValidationError({"otp_code": "Invalid verification code."})

        user.mfa_enabled = True
        user.mfa_enabled_at = timezone.now()
        user.save(update_fields=["mfa_enabled", "mfa_enabled_at"])
        _log(request, user, AuditAction.MFA_ENABLED)
        return Response(status=204)


class UserDirectoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only staff directory consumed by other modules' provider/staff
    pickers (pharmacy prescriber, lab/radiology ordering provider, theatre
    surgeon, etc.). No module_code/ModulePermission gate -- any
    authenticated staff member may look up colleagues by name; the
    UserDirectorySerializer already excludes anything sensitive."""

    queryset = User.objects.filter(is_active=True).select_related("branch").prefetch_related("roles")
    serializer_class = UserDirectorySerializer
    lookup_field = "public_id"
    permission_classes = [IsAuthenticated]
    filterset_fields = ["branch"]
    search_fields = ["email", "first_name", "last_name"]
    ordering_fields = ["last_name", "first_name"]


class MFADisableView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = MFADisableSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        if not user.check_password(serializer.validated_data["password"]):
            raise ValidationError({"password": "Incorrect password."})

        user.mfa_enabled = False
        user.mfa_secret = ""
        user.mfa_enabled_at = None
        user.save(update_fields=["mfa_enabled", "mfa_secret", "mfa_enabled_at"])
        _log(request, user, AuditAction.MFA_DISABLED)
        return Response(status=204)
