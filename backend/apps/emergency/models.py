from django.conf import settings
from django.db import models

from apps.core.models import BaseModel, BranchScopedModel


class EmergencyCase(BaseModel, BranchScopedModel):
    class TriageLevel(models.TextChoices):
        ONE = "1", "Resuscitation"
        TWO = "2", "Emergent"
        THREE = "3", "Urgent"
        FOUR = "4", "Less Urgent"
        FIVE = "5", "Non-Urgent"

    class Status(models.TextChoices):
        WAITING = "waiting", "Waiting"
        IN_TREATMENT = "in_treatment", "In Treatment"
        ADMITTED = "admitted", "Admitted"
        DISCHARGED = "discharged", "Discharged"
        TRANSFERRED = "transferred", "Transferred"

    patient = models.ForeignKey("patients.Patient", on_delete=models.PROTECT, related_name="emergency_cases")
    triage_level = models.CharField(max_length=1, choices=TriageLevel.choices)
    arrival_time = models.DateTimeField(auto_now_add=True)
    chief_complaint = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.WAITING)
    attending_provider = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="emergency_cases",
    )

    class Meta:
        ordering = ["-arrival_time"]

    def __str__(self) -> str:
        return f"{self.patient} - triage {self.triage_level}"
