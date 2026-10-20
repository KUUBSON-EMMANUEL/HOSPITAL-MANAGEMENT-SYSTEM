from django.conf import settings
from django.contrib.postgres.constraints import ExclusionConstraint
from django.contrib.postgres.fields import DateTimeRangeField, RangeBoundary, RangeOperators
from django.db import models
from django.db.models import Func, Q

from apps.authentication.constants import ModuleCode
from apps.core.models import BaseModel, BranchScopedModel


class TsTzRange(Func):
    function = "TSTZRANGE"
    output_field = DateTimeRangeField()


# Statuses that free up the provider's time slot.
INACTIVE_STATUSES = ["cancelled", "no_show"]


class Appointment(BaseModel, BranchScopedModel):
    class AppointmentType(models.TextChoices):
        NEW_VISIT = "new_visit", "New Visit"
        FOLLOW_UP = "follow_up", "Follow-up"
        PROCEDURE = "procedure", "Procedure"
        CONSULTATION = "consultation", "Consultation"

    class Status(models.TextChoices):
        SCHEDULED = "scheduled", "Scheduled"
        CONFIRMED = "confirmed", "Confirmed"
        CHECKED_IN = "checked_in", "Checked In"
        IN_PROGRESS = "in_progress", "In Progress"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"
        NO_SHOW = "no_show", "No Show"

    patient = models.ForeignKey("patients.Patient", on_delete=models.PROTECT, related_name="appointments")
    provider = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="provider_appointments"
    )
    module = models.CharField(
        max_length=32,
        choices=ModuleCode.choices,
        blank=True,
        help_text="Which department this appointment is for, e.g. RADIOLOGY.",
    )
    appointment_type = models.CharField(max_length=32, choices=AppointmentType.choices)
    scheduled_start = models.DateTimeField()
    scheduled_end = models.DateTimeField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SCHEDULED)
    reason = models.TextField(blank=True)
    cancellation_reason = models.TextField(blank=True)

    class Meta:
        ordering = ["scheduled_start"]
        indexes = [models.Index(fields=["provider", "scheduled_start"])]
        constraints = [
            # Database-level guard against double-booking: a provider cannot
            # have two active appointments whose [start, end) ranges overlap.
            # The serializer checks this too, for a friendly error message.
            ExclusionConstraint(
                name="appointment_no_provider_overlap",
                expressions=[
                    (TsTzRange("scheduled_start", "scheduled_end", RangeBoundary()), RangeOperators.OVERLAPS),
                    ("provider", RangeOperators.EQUAL),
                ],
                condition=Q(deleted_at__isnull=True) & ~Q(status__in=INACTIVE_STATUSES),
            ),
        ]

    def __str__(self) -> str:
        return f"{self.patient} with {self.provider} @ {self.scheduled_start:%Y-%m-%d %H:%M}"
