from django.contrib import admin

from .models import Consultation


@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ["patient", "provider", "status", "created_at", "branch"]
    list_filter = ["status", "branch"]
    search_fields = ["patient__first_name", "patient__last_name", "chief_complaint"]
