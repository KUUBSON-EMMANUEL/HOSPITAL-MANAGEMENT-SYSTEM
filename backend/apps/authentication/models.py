from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from apps.core.models import TimeStampedModel, UUIDPublicIDModel

from .constants import ModuleCode, PermissionAction, RoleCode


class Role(TimeStampedModel, UUIDPublicIDModel):
    """One row per RoleCode; a user's actual authorization comes from the
    Permission rows attached to whichever roles they're assigned (see
    User.roles, User.has_module_permission)."""

    code = models.CharField(max_length=32, choices=RoleCode.choices, unique=True)
    name = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["code"]

    def __str__(self) -> str:
        return self.name or self.get_code_display()

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.get_code_display()
        super().save(*args, **kwargs)


class Permission(TimeStampedModel):
    """Grants a Role the ability to perform `action` within `module`."""

    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="permissions")
    module = models.CharField(max_length=32, choices=ModuleCode.choices)
    action = models.CharField(max_length=16, choices=PermissionAction.choices)

    class Meta:
        ordering = ["module", "action"]
        constraints = [
            models.UniqueConstraint(fields=["role", "module", "action"], name="unique_role_module_action")
        ]

    def __str__(self) -> str:
        return f"{self.role.code}: {self.module}.{self.action}"


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("must_change_password", False)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(email, password, **extra_fields)


class User(TimeStampedModel, UUIDPublicIDModel, AbstractBaseUser, PermissionsMixin):
    """
    Staff account. Patients are never represented as Users -- see
    apps.patients.models.Patient for patient records, which carry no login
    credentials. Authorization is via Role -> Permission (see
    has_module_permission), not Django's built-in Group/Permission tables
    (kept only via PermissionsMixin for is_superuser + admin-site support).
    """

    email = models.EmailField(unique=True, db_index=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20, blank=True)
    employee_id = models.CharField(max_length=32, unique=True, null=True, blank=True)

    branch = models.ForeignKey(
        "branches.Branch",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="staff_users",
        help_text="Null for cross-branch roles (e.g. SUPER_ADMIN, IT_ADMIN).",
    )
    roles = models.ManyToManyField(Role, related_name="users", blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    must_change_password = models.BooleanField(default=True)
    password_changed_at = models.DateTimeField(null=True, blank=True)

    mfa_enabled = models.BooleanField(default=False)
    mfa_secret = models.CharField(max_length=64, blank=True)
    mfa_enabled_at = models.DateTimeField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ["last_name", "first_name"]

    def __str__(self) -> str:
        return self.email

    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self) -> str:
        return self.first_name

    def has_role(self, *role_codes) -> bool:
        if self.is_superuser:
            return True
        return self.roles.filter(code__in=role_codes, is_active=True).exists()

    def has_module_permission(self, module_code, action) -> bool:
        """
        Backs apps.core.permissions.ModulePermission -- called on every
        permission-gated API request. One indexed EXISTS query regardless of
        role count (role__in is a join, not N+1).
        TODO: memoize per-request (self._permission_cache) if a single
        request ends up calling this many times, or move to a Redis-backed
        cache keyed by user id, invalidated on Role/Permission/roles changes,
        if this becomes a hot path under load.
        """
        if self.is_superuser:
            return True
        return Permission.objects.filter(
            role__in=self.roles.filter(is_active=True), module=module_code, action=action
        ).exists()
