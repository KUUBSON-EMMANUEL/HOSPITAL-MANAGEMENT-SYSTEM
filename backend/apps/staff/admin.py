from django.contrib import admin

from .models import StaffProfile


@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "department", "designation", "employment_status", "hire_date"]
    list_filter = ["employment_status", "department"]
    search_fields = ["user__email", "user__first_name", "user__last_name", "department", "designation"]
