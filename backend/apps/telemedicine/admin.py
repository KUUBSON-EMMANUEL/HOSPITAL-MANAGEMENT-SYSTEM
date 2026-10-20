from django.contrib import admin

from .models import TelemedicineSession


@admin.register(TelemedicineSession)
class TelemedicineSessionAdmin(admin.ModelAdmin):
    list_display = ["patient", "provider", "status", "scheduled_start", "branch"]
    list_filter = ["branch", "status"]
    search_fields = ["patient__first_name", "patient__last_name"]
