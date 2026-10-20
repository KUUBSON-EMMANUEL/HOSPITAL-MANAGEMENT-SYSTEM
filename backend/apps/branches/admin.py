from django.contrib import admin

from .models import Branch


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ["code", "name", "city", "country", "is_main_branch", "is_active", "bed_capacity"]
    list_filter = ["is_active", "is_main_branch", "country"]
    search_fields = ["code", "name", "city"]
