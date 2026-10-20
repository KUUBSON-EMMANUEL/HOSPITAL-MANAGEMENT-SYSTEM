from django.core.validators import RegexValidator
from django.db import models

from apps.core.models import TimeStampedModel, UUIDPublicIDModel


class Branch(TimeStampedModel, UUIDPublicIDModel):
    """
    A physical hospital facility within the hospital group. Every clinical
    and operational record is scoped to a branch (see BranchScopedModel),
    enabling multi-branch hospital support with per-branch data isolation
    and cross-branch reporting for group administrators.
    """

    code = models.CharField(
        max_length=10,
        unique=True,
        validators=[RegexValidator(r"^[A-Z0-9]{2,10}$", "Branch code must be 2-10 uppercase letters/digits.")],
        help_text="Short unique code used as a prefix in patient/record IDs, e.g. MAIN, EAST.",
    )
    name = models.CharField(max_length=150)
    is_main_branch = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state_region = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank=True)

    phone_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True)

    timezone = models.CharField(max_length=64, default="UTC")
    license_number = models.CharField(max_length=100, blank=True)
    bed_capacity = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["is_main_branch"],
                condition=models.Q(is_main_branch=True),
                name="unique_main_branch",
                violation_error_message="Only one branch may be marked as the main branch.",
            )
        ]

    def __str__(self) -> str:
        return f"{self.name} ({self.code})"
