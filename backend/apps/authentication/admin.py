from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import Permission, Role, User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    ordering = ["email"]
    list_display = ["email", "first_name", "last_name", "branch", "is_active", "is_staff", "mfa_enabled"]
    list_filter = ["is_active", "is_staff", "mfa_enabled", "branch"]
    search_fields = ["email", "first_name", "last_name", "employee_id"]
    filter_horizontal = ["roles", "groups", "user_permissions"]
    readonly_fields = ["mfa_enabled_at", "password_changed_at", "last_login", "created_at", "updated_at"]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "phone_number", "employee_id", "branch")}),
        (
            "Roles & permissions",
            {"fields": ("roles", "is_active", "is_staff", "is_superuser", "groups", "user_permissions")},
        ),
        ("MFA", {"fields": ("mfa_enabled", "mfa_enabled_at")}),
        ("Password policy", {"fields": ("must_change_password", "password_changed_at")}),
        ("Important dates", {"fields": ("last_login", "created_at", "updated_at")}),
    )
    add_fieldsets = ((None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ["code", "name", "is_active"]
    search_fields = ["code", "name"]


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ["role", "module", "action"]
    list_filter = ["module", "action"]
    autocomplete_fields = ["role"]
