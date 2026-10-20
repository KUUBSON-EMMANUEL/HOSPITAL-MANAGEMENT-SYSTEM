from django.conf import settings
from django.db import models

from apps.core.models import BaseModel, BranchScopedModel, max_trailing_number, next_sequence_value


class Patient(BaseModel, BranchScopedModel):
    """A registered patient. Patients never log in (no User account) --
    this model carries no credentials, only demographic/clinical-contact
    data. patient_number is server-generated in the serializer, not here,
    to keep the model free of request-time side effects."""

    class Sex(models.TextChoices):
        MALE = "M", "Male"
        FEMALE = "F", "Female"
        OTHER = "O", "Other"

    class BloodType(models.TextChoices):
        A_POS = "A+", "A+"
        A_NEG = "A-", "A-"
        B_POS = "B+", "B+"
        B_NEG = "B-", "B-"
        AB_POS = "AB+", "AB+"
        AB_NEG = "AB-", "AB-"
        O_POS = "O+", "O+"
        O_NEG = "O-", "O-"
        UNKNOWN = "unknown", "Unknown"

    patient_number = models.CharField(max_length=32, unique=True, db_index=True, editable=False)

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    middle_name = models.CharField(max_length=150, blank=True)
    date_of_birth = models.DateField()
    sex = models.CharField(max_length=1, choices=Sex.choices)
    blood_type = models.CharField(max_length=10, choices=BloodType.choices, blank=True)

    phone_number = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address_line1 = models.CharField(max_length=255, blank=True)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state_region = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)

    emergency_contact_name = models.CharField(max_length=150, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    emergency_contact_relationship = models.CharField(max_length=50, blank=True)

    allergies = models.JSONField(
        default=list,
        blank=True,
        help_text="List of substance strings, e.g. [\"penicillin\", \"peanuts\"].",
    )

    registration_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["-registration_date"]
        indexes = [models.Index(fields=["last_name", "first_name"])]

    def __str__(self) -> str:
        return f"{self.patient_number} - {self.first_name} {self.last_name}"


def generate_patient_number(branch) -> str:
    """
    Called from PatientSerializer.create(), not Patient.save(), to keep the
    model free of request-time side effects. Uses a row-locked counter so
    simultaneous registrations on the same branch never collide.
    """
    prefix = settings.HMS_PATIENT_ID_PREFIX
    sequence = next_sequence_value(
        f"patient:{branch.pk}",
        seed=lambda: max_trailing_number(
            Patient.all_objects.filter(branch=branch).values_list("patient_number", flat=True)
        ),
    )
    return f"{prefix}-{branch.code}-{sequence:06d}"
