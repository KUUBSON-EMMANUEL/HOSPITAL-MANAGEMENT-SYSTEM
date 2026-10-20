from django.contrib import admin

from .models import TheatreBooking


@admin.register(TheatreBooking)
class TheatreBookingAdmin(admin.ModelAdmin):
    list_display = ["procedure_name", "patient", "surgeon", "status", "scheduled_start", "branch"]
    list_filter = ["branch", "status"]
    search_fields = ["procedure_name", "patient__first_name", "patient__last_name"]
