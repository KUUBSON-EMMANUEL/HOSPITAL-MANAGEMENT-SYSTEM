from django.conf import settings
from django.db import models

from apps.core.models import BaseModel, BranchScopedModel


class NursingNote(BaseModel, BranchScopedModel):
    class Shift(models.TextChoices):
        MORNING = "morning", "Morning"
        AFTERNOON = "afternoon", "Afternoon"
        NIGHT = "night", "Night"

    patient = models.ForeignKey("patients.Patient", on_delete=models.PROTECT, related_name="nursing_notes")
    encounter = models.ForeignKey(
        "ehr.Encounter",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="nursing_notes",
    )
    nurse = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="nursing_notes"
    )
    note = models.TextField()
    shift = models.CharField(max_length=20, choices=Shift.choices)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Nursing note for {self.patient} ({self.shift})"
