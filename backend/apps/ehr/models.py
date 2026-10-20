from django.conf import settings
from django.db import models

from apps.core.models import BaseModel, BranchScopedModel


class Encounter(BaseModel, BranchScopedModel):
    """Connective-tissue model tying a care episode together -- not a
    FHIR-style clinical data warehouse. Consultations/lab orders/etc. link
    back to an Encounter; the encounter itself just tracks who/when/why."""

    class EncounterType(models.TextChoices):
        OUTPATIENT = "outpatient", "Outpatient"
        INPATIENT = "inpatient", "Inpatient"
        EMERGENCY = "emergency", "Emergency"
        TELEMEDICINE = "telemedicine", "Telemedicine"

    class Status(models.TextChoices):
        OPEN = "open", "Open"
        CLOSED = "closed", "Closed"

    patient = models.ForeignKey("patients.Patient", on_delete=models.PROTECT, related_name="encounters")
    appointment = models.ForeignKey(
        "appointments.Appointment", null=True, blank=True, on_delete=models.SET_NULL, related_name="encounters"
    )
    attending_provider = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="attended_encounters"
    )
    encounter_type = models.CharField(max_length=20, choices=EncounterType.choices)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.OPEN)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    chief_complaint = models.TextField(blank=True)

    class Meta:
        ordering = ["-started_at"]

    def __str__(self) -> str:
        return f"{self.patient} - {self.encounter_type} ({self.started_at:%Y-%m-%d})"


class VitalSigns(BaseModel, BranchScopedModel):
    patient = models.ForeignKey("patients.Patient", on_delete=models.PROTECT, related_name="vital_signs")
    encounter = models.ForeignKey(
        Encounter, null=True, blank=True, on_delete=models.SET_NULL, related_name="vital_signs"
    )
    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="recorded_vitals"
    )
    recorded_at = models.DateTimeField(auto_now_add=True)

    temperature_celsius = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    pulse_bpm = models.PositiveSmallIntegerField(null=True, blank=True)
    respiratory_rate = models.PositiveSmallIntegerField(null=True, blank=True)
    systolic_bp = models.PositiveSmallIntegerField(null=True, blank=True)
    diastolic_bp = models.PositiveSmallIntegerField(null=True, blank=True)
    spo2_percent = models.PositiveSmallIntegerField(null=True, blank=True)
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    height_cm = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)

    class Meta:
        ordering = ["-recorded_at"]
        verbose_name_plural = "Vital signs"

    def __str__(self) -> str:
        return f"Vitals for {self.patient} @ {self.recorded_at:%Y-%m-%d %H:%M}"
