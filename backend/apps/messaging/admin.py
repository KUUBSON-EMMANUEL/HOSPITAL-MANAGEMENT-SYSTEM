from django.contrib import admin

from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ["sender", "recipient", "read_at", "created_at"]
    list_filter = ["read_at"]
    search_fields = ["sender__email", "recipient__email", "body"]
