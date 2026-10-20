from django.contrib import admin

from .models import ImagingOrder


@admin.register(ImagingOrder)
class ImagingOrderAdmin(admin.ModelAdmin):
    list_display = ["patient", "modality", "ordering_provider", "status", "ordered_at", "branch"]
    list_filter = ["branch", "modality", "status"]
    search_fields = ["patient__first_name", "patient__last_name"]
