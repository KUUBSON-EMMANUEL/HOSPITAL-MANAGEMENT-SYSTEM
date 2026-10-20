from django.conf import settings
from django.db import models

from apps.core.models import BaseModel, BranchScopedModel


class Consultation(BaseModel, BranchScopedModel):
    """SOAP-note consultation record. diagnosis is a structured JSON list
    ([{"code": "...", "description": "..."}]) rather than a real ICD-10
    lookup table -- that table is explicitly out of scope this pass."""

    class Status(models.TextChoices):
        IN_PROGRESS = "in_progress", "In Progress"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    patient = models.ForeignKey("patients.Patient", on_delete=models.PROTECT, related_name="consultations")
    provider = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="consultations"
    )
    appointment = models.ForeignKey(
        "appointments.Appointment", null=True, blank=True, on_delete=models.SET_NULL, related_name="consultations"
    )
    encounter = models.ForeignKey(
        "ehr.Encounter", null=True, blank=True, on_delete=models.SET_NULL, related_name="consultations"
    )

    chief_complaint = models.TextField(blank=True)
    subjective = models.TextField(blank=True)
    objective = models.TextField(blank=True)
    assessment = models.TextField(blank=True)
    plan = models.TextField(blank=True)
    diagnosis = models.JSONField(
        default=list, blank=True, help_text='List of {"code": "...", "description": "..."} objects.'
    )
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.IN_PROGRESS)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Consultation: {self.patient} with {self.provider} ({self.created_at:%Y-%m-%d})"
