from django.contrib import admin

from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ["patient_number", "first_name", "last_name", "sex", "date_of_birth", "branch", "phone_number"]
    list_filter = ["branch", "sex", "blood_type"]
    search_fields = ["patient_number", "first_name", "last_name", "phone_number", "email"]
