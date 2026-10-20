from django.contrib import admin

from .models import InsurancePolicy


@admin.register(InsurancePolicy)
class InsurancePolicyAdmin(admin.ModelAdmin):
    list_display = ["policy_number", "provider_name", "patient", "status", "valid_from", "valid_to", "branch"]
    list_filter = ["branch", "status"]
    search_fields = ["policy_number", "provider_name", "patient__first_name", "patient__last_name"]
