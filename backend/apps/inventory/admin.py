from django.contrib import admin

from .models import InventoryItem, StockMovement


@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ["name", "sku", "unit", "quantity_on_hand", "reorder_level", "branch"]
    list_filter = ["branch"]
    search_fields = ["name", "sku"]


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ["item", "movement_type", "quantity", "recorded_by", "created_at"]
    list_filter = ["movement_type"]
    search_fields = ["item__name", "item__sku", "reason"]
