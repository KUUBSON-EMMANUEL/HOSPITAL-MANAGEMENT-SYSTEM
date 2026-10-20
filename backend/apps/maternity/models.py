from django.conf import settings
from django.db import models

from apps.core.models import BaseModel, BranchScopedModel


class MaternityRecord(BaseModel, BranchScopedModel):
    class Status(models.TextChoices):
        ANTENATAL = "antenatal", "Antenatal"
        DELIVERED = "delivered", "Delivered"
        POSTNATAL = "postnatal", "Postnatal"

    patient = models.ForeignKey(
        "patients.Patient", on_delete=models.PROTECT, related_name="maternity_records"
    )
    attending_provider = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="maternity_records"
    )
    expected_delivery_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ANTENATAL)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Maternity record for {self.patient}"
