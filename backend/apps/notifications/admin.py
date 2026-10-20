from django.contrib import admin

from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ["title", "recipient", "channel", "status", "sent_at", "created_at"]
    list_filter = ["channel", "status"]
    search_fields = ["title", "body", "recipient__email"]
