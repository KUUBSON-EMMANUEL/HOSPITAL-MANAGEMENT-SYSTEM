from django.conf import settings
from django.db import models

from apps.core.models import BaseModel, BranchScopedModel


class TheatreBooking(BaseModel, BranchScopedModel):
    class Status(models.TextChoices):
        SCHEDULED = "scheduled", "Scheduled"
        IN_PROGRESS = "in_progress", "In Progress"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    patient = models.ForeignKey("patients.Patient", on_delete=models.PROTECT, related_name="theatre_bookings")
    surgeon = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="theatre_bookings"
    )
    procedure_name = models.CharField(max_length=255)
    scheduled_start = models.DateTimeField()
    scheduled_end = models.DateTimeField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SCHEDULED)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["scheduled_start"]

    def __str__(self) -> str:
        return f"{self.procedure_name} - {self.patient}"
