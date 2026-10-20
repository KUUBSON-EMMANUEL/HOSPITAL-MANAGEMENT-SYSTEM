from django.contrib import admin

from .models import EmergencyCase


@admin.register(EmergencyCase)
class EmergencyCaseAdmin(admin.ModelAdmin):
    list_display = ["patient", "triage_level", "status", "attending_provider", "arrival_time", "branch"]
    list_filter = ["branch", "triage_level", "status"]
    search_fields = ["patient__first_name", "patient__last_name", "chief_complaint"]
