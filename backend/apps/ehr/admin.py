from django.contrib import admin

from .models import Encounter, VitalSigns


@admin.register(Encounter)
class EncounterAdmin(admin.ModelAdmin):
    list_display = ["patient", "encounter_type", "status", "attending_provider", "started_at", "branch"]
    list_filter = ["encounter_type", "status", "branch"]
    search_fields = ["patient__first_name", "patient__last_name"]


@admin.register(VitalSigns)
class VitalSignsAdmin(admin.ModelAdmin):
    list_display = ["patient", "recorded_at", "pulse_bpm", "systolic_bp", "diastolic_bp", "spo2_percent"]
    list_filter = ["branch"]
    search_fields = ["patient__first_name", "patient__last_name"]
