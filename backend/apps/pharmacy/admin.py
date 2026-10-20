from django.contrib import admin

from .models import Prescription, PrescriptionItem


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ["patient", "prescriber", "status", "branch", "created_at"]
    list_filter = ["branch", "status"]
    search_fields = ["patient__first_name", "patient__last_name", "prescriber__email"]


@admin.register(PrescriptionItem)
class PrescriptionItemAdmin(admin.ModelAdmin):
    list_display = ["drug_name", "dosage", "frequency", "duration", "quantity", "prescription"]
    search_fields = ["drug_name", "prescription__patient__first_name", "prescription__patient__last_name"]
