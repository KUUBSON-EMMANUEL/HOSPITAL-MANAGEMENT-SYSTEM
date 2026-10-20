from django.conf import settings
from django.db import models

from apps.core.models import BaseModel, BranchScopedModel


class TelemedicineSession(BaseModel, BranchScopedModel):
    class Status(models.TextChoices):
        SCHEDULED = "scheduled", "Scheduled"
        IN_PROGRESS = "in_progress", "In Progress"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    patient = models.ForeignKey(
        "patients.Patient", on_delete=models.PROTECT, related_name="telemedicine_sessions"
    )
    provider = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="telemedicine_sessions"
    )
    scheduled_start = models.DateTimeField()
    scheduled_end = models.DateTimeField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SCHEDULED)
    session_url = models.URLField(blank=True)
    session_token = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["scheduled_start"]

    def __str__(self) -> str:
        return f"Telemedicine {self.patient} with {self.provider}"
