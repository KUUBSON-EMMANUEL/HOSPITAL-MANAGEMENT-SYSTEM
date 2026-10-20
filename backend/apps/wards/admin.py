from django.contrib import admin

from .models import Bed


@admin.register(Bed)
class BedAdmin(admin.ModelAdmin):
    list_display = ["ward_name", "bed_number", "bed_type", "status", "current_patient", "branch"]
    list_filter = ["branch", "bed_type", "status"]
    search_fields = ["ward_name", "bed_number"]
