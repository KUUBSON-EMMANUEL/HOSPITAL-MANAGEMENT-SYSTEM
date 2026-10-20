from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.core.serializers import PublicIdRelatedField

from .models import Role

User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Adds branch/role claims to the JWT. Referenced by
    SIMPLE_JWT['TOKEN_OBTAIN_SERIALIZER']; the actual login endpoint
    (LoginView) calls get_token() directly rather than using this
    serializer's validate(), so it can branch into the MFA challenge flow --
    but this stays self-consistent in case anything else obtains tokens
    through the standard simplejwt view."""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        token["branch_id"] = str(user.branch.public_id) if user.branch_id else None
        token["roles"] = list(user.roles.filter(is_active=True).values_list("code", flat=True))
        return token


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ["public_id", "code", "name", "description", "is_active"]
        read_only_fields = ["public_id"]


class UserProfileSerializer(serializers.ModelSerializer):
    roles = serializers.SlugRelatedField(slug_field="code", many=True, read_only=True)
    branch = serializers.SlugRelatedField(slug_field="public_id", read_only=True)

    class Meta:
        model = User
        fields = [
            "public_id", "email", "first_name", "last_name", "phone_number", "employee_id",
            "branch", "roles", "is_active", "is_staff", "must_change_password", "mfa_enabled",
            "created_at", "updated_at",
        ]
        read_only_fields = fields


class UserDirectorySerializer(serializers.ModelSerializer):
    """Lightweight, non-sensitive listing used to populate staff/provider
    pickers across other modules (pharmacy prescriber, lab ordering
    provider, theatre surgeon, etc.) -- deliberately excludes
    must_change_password/mfa_enabled/employee_id."""

    roles = serializers.SlugRelatedField(slug_field="code", many=True, read_only=True)
    branch = PublicIdRelatedField(read_only=True)

    class Meta:
        model = User
        fields = ["public_id", "email", "first_name", "last_name", "branch", "roles"]
        read_only_fields = fields


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={"input_type": "password"})


class MFAVerifySerializer(serializers.Serializer):
    challenge_token = serializers.CharField()
    otp_code = serializers.CharField(min_length=6, max_length=6)


class MFAVerifySetupSerializer(serializers.Serializer):
    otp_code = serializers.CharField(min_length=6, max_length=6)


class MFADisableSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate_new_password(self, value):
        validate_password(value, user=self.context["request"].user)
        return value
