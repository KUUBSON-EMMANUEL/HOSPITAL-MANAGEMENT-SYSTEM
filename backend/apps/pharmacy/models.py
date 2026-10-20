from django.conf import settings
from django.db import models

from apps.core.models import BaseModel, BranchScopedModel


class Prescription(BaseModel, BranchScopedModel):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        DISPENSED = "dispensed", "Dispensed"
        PARTIALLY_DISPENSED = "partially_dispensed", "Partially Dispensed"
        CANCELLED = "cancelled", "Cancelled"

    patient = models.ForeignKey("patients.Patient", on_delete=models.PROTECT, related_name="prescriptions")
    prescriber = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="prescriptions"
    )
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Prescription for {self.patient} by {self.prescriber}"


class PrescriptionItem(BaseModel):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name="items")
    drug_name = models.CharField(max_length=200)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.drug_name} ({self.prescription_id})"
