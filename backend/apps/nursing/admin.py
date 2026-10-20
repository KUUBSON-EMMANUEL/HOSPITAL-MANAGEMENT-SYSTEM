from django.contrib import admin

from .models import NursingNote


@admin.register(NursingNote)
class NursingNoteAdmin(admin.ModelAdmin):
    list_display = ["patient", "nurse", "shift", "encounter", "branch", "created_at"]
    list_filter = ["branch", "shift"]
    search_fields = ["note", "patient__first_name", "patient__last_name"]
