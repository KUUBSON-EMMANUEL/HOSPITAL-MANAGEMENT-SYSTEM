from django.contrib import admin

from .models import MaternityRecord


@admin.register(MaternityRecord)
class MaternityRecordAdmin(admin.ModelAdmin):
    list_display = ["patient", "attending_provider", "status", "expected_delivery_date", "branch"]
    list_filter = ["branch", "status"]
    search_fields = ["patient__first_name", "patient__last_name"]
