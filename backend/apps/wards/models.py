from django.db import models

from apps.core.models import BaseModel, BranchScopedModel


class Bed(BaseModel, BranchScopedModel):
    class BedType(models.TextChoices):
        GENERAL = "general", "General"
        PRIVATE = "private", "Private"
        ICU = "icu", "ICU"
        ISOLATION = "isolation", "Isolation"

    class Status(models.TextChoices):
        AVAILABLE = "available", "Available"
        OCCUPIED = "occupied", "Occupied"
        MAINTENANCE = "maintenance", "Maintenance"
        RESERVED = "reserved", "Reserved"

    ward_name = models.CharField(max_length=100)
    bed_number = models.CharField(max_length=20)
    bed_type = models.CharField(max_length=20, choices=BedType.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.AVAILABLE)
    current_patient = models.ForeignKey(
        "patients.Patient",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="current_bed",
    )

    class Meta:
        ordering = ["ward_name", "bed_number"]
        unique_together = [("branch", "ward_name", "bed_number")]

    def __str__(self) -> str:
        return f"{self.ward_name} / Bed {self.bed_number}"
