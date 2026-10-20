from django.db import models

from apps.core.models import BaseModel, BranchScopedModel


class InsurancePolicy(BaseModel, BranchScopedModel):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        EXPIRED = "expired", "Expired"
        CANCELLED = "cancelled", "Cancelled"

    patient = models.ForeignKey(
        "patients.Patient", on_delete=models.PROTECT, related_name="insurance_policies"
    )
    provider_name = models.CharField(max_length=200)
    policy_number = models.CharField(max_length=100)
    coverage_type = models.CharField(max_length=100, blank=True)
    valid_from = models.DateField()
    valid_to = models.DateField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)

    class Meta:
        ordering = ["-created_at"]
        unique_together = [("provider_name", "policy_number")]

    def __str__(self) -> str:
        return f"{self.provider_name} - {self.policy_number} ({self.patient})"
