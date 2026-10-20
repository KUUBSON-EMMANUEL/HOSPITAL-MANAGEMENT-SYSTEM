from django.contrib import admin

from .models import LabOrder


@admin.register(LabOrder)
class LabOrderAdmin(admin.ModelAdmin):
    list_display = ["test_name", "patient", "ordering_provider", "status", "ordered_at", "branch"]
    list_filter = ["branch", "status"]
    search_fields = ["test_name", "patient__first_name", "patient__last_name"]
