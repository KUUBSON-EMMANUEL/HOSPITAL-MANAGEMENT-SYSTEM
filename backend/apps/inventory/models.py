from django.conf import settings
from django.db import models

from apps.core.models import BaseModel, BranchScopedModel


class InventoryItem(BaseModel, BranchScopedModel):
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=64, unique=True)
    unit = models.CharField(max_length=50, help_text='e.g. "box", "vial".')
    quantity_on_hand = models.PositiveIntegerField(default=0)
    reorder_level = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.name} ({self.sku})"


class StockMovement(BaseModel):
    class MovementType(models.TextChoices):
        INBOUND = "inbound", "Inbound"
        OUTBOUND = "outbound", "Outbound"
        ADJUSTMENT = "adjustment", "Adjustment"

    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name="movements")
    movement_type = models.CharField(max_length=20, choices=MovementType.choices)
    quantity = models.IntegerField(help_text="Can be negative for outbound/adjustment movements.")
    reason = models.CharField(max_length=255, blank=True)
    recorded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="stock_movements")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.get_movement_type_display()} {self.quantity} - {self.item}"
