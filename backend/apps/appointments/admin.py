from django.contrib import admin

from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ["patient", "provider", "scheduled_start", "status", "appointment_type", "branch"]
    list_filter = ["status", "appointment_type", "branch"]
    search_fields = ["patient__first_name", "patient__last_name", "provider__email"]
