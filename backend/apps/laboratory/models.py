from django.conf import settings
from django.db import models

from apps.core.models import BaseModel, BranchScopedModel


class LabOrder(BaseModel, BranchScopedModel):
    class Status(models.TextChoices):
        ORDERED = "ordered", "Ordered"
        COLLECTED = "collected", "Collected"
        IN_PROGRESS = "in_progress", "In Progress"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    patient = models.ForeignKey("patients.Patient", on_delete=models.PROTECT, related_name="lab_orders")
    ordering_provider = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="lab_orders"
    )
    test_name = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ORDERED)
    ordered_at = models.DateTimeField(auto_now_add=True)
    result_value = models.CharField(max_length=255, blank=True)
    result_text = models.TextField(blank=True)
    reference_range = models.CharField(max_length=100, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-ordered_at"]

    def __str__(self) -> str:
        return f"{self.test_name} for {self.patient}"
