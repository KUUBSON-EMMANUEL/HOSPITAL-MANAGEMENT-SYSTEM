from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from apps.authentication.constants import ModuleCode
from apps.core.permissions import ModulePermission

from .models import Branch
from .serializers import BranchSerializer


class BranchViewSet(viewsets.ModelViewSet):
    """
    Manages hospital branches for multi-branch hospital groups. Branch
    administration is a super-admin/branch-admin concern -- clinical staff
    consume the branch list read-only via their own profile/branch context.
    """

    queryset = Branch.objects.all().order_by("name")
    serializer_class = BranchSerializer
    lookup_field = "public_id"
    permission_classes = [ModulePermission]
    module_code = ModuleCode.BRANCHES
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name", "code", "city", "country"]
    ordering_fields = ["name", "created_at", "bed_capacity"]
