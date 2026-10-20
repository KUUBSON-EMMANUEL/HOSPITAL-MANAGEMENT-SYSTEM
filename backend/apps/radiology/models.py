from django.conf import settings
from django.db import models

from apps.core.models import BaseModel, BranchScopedModel


class ImagingOrder(BaseModel, BranchScopedModel):
    class Modality(models.TextChoices):
        XRAY = "xray", "X-Ray"
        CT = "ct", "CT Scan"
        MRI = "mri", "MRI"
        ULTRASOUND = "ultrasound", "Ultrasound"

    class Status(models.TextChoices):
        ORDERED = "ordered", "Ordered"
        SCHEDULED = "scheduled", "Scheduled"
        IN_PROGRESS = "in_progress", "In Progress"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    patient = models.ForeignKey("patients.Patient", on_delete=models.PROTECT, related_name="imaging_orders")
    ordering_provider = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="imaging_orders"
    )
    modality = models.CharField(max_length=20, choices=Modality.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ORDERED)
    ordered_at = models.DateTimeField(auto_now_add=True)
    findings = models.TextField(blank=True)
    report = models.TextField(blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-ordered_at"]

    def __str__(self) -> str:
        return f"{self.get_modality_display()} for {self.patient}"
