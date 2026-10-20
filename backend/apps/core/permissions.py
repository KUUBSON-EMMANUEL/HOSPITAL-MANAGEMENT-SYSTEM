from rest_framework.permissions import SAFE_METHODS, BasePermission

from apps.authentication.constants import PermissionAction, RoleCode

_METHOD_ACTION_MAP = {
    "GET": PermissionAction.VIEW,
    "HEAD": PermissionAction.VIEW,
    "OPTIONS": PermissionAction.VIEW,
    "POST": PermissionAction.CREATE,
    "PUT": PermissionAction.EDIT,
    "PATCH": PermissionAction.EDIT,
    "DELETE": PermissionAction.DELETE,
}


class ModulePermission(BasePermission):
    """
    Generic RBAC permission backend used by every module's ViewSets.

    A view opts in by declaring `module_code` (from ModuleCode) and,
    optionally, a per-action override map `action_permission_map`
    (e.g. {"approve": PermissionAction.APPROVE}). Access is granted if the
    authenticated user's assigned role(s) carry a Permission row for that
    (module, action) pair -- see apps.authentication.models.Role/Permission.
    """

    def has_permission(self, request, view):
        user = request.user
        if not (user and user.is_authenticated and user.is_active):
            return False
        if user.is_superuser:
            return True

        module_code = getattr(view, "module_code", None)
        if module_code is None:
            # A view that hasn't declared its module is a configuration bug,
            # not an access grant -- fail closed.
            return False

        action = getattr(view, "action", None)
        override_map = getattr(view, "action_permission_map", {})
        permission_action = override_map.get(action) or _METHOD_ACTION_MAP.get(request.method)
        if permission_action is None:
            return False

        return user.has_module_permission(module_code, permission_action)


class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and (user.is_superuser or user.has_role(RoleCode.SUPER_ADMIN)))


class IsBranchAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and (user.is_superuser or user.has_role(RoleCode.SUPER_ADMIN, RoleCode.BRANCH_ADMIN))
        )


class ReadOnlyOrModulePermission(ModulePermission):
    """Allows read access to any authenticated staff member with module VIEW rights,
    but still enforces module-specific write permissions for mutating requests."""

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return super().has_permission(request, view)
        return super().has_permission(request, view)


class SameBranchObjectPermission(BasePermission):
    """
    Object-level check enforcing that non-superadmin users may only act on
    records belonging to their assigned branch, supporting multi-branch data
    isolation even when list-level querysets are already branch-filtered.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_superuser or user.has_role(RoleCode.SUPER_ADMIN):
            return True
        obj_branch = getattr(obj, "branch_id", None)
        return obj_branch is None or obj_branch == user.branch_id
