from django.db import models

from apps.authentication.constants import ModuleCode
from apps.core.models import BaseModel, BranchScopedModel, max_trailing_number, next_sequence_value


class Invoice(BaseModel, BranchScopedModel):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        ISSUED = "issued", "Issued"
        PARTIALLY_PAID = "partially_paid", "Partially Paid"
        PAID = "paid", "Paid"
        VOID = "void", "Void"

    patient = models.ForeignKey("patients.Patient", on_delete=models.PROTECT, related_name="invoices")
    invoice_number = models.CharField(max_length=32, unique=True, db_index=True, editable=False)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    due_date = models.DateField(null=True, blank=True)
    issued_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.invoice_number} ({self.patient})"


def generate_invoice_number(branch) -> str:
    """
    Called from InvoiceSerializer.create(), not Invoice.save(), to keep the
    model free of request-time side effects. Uses a row-locked counter so
    simultaneous invoice creations on the same branch never collide.
    """
    sequence = next_sequence_value(
        f"invoice:{branch.pk}",
        seed=lambda: max_trailing_number(
            Invoice.all_objects.filter(branch=branch).values_list("invoice_number", flat=True)
        ),
    )
    return f"INV-{branch.code}-{sequence:06d}"


class InvoiceLineItem(BaseModel):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="line_items")
    description = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    line_total = models.DecimalField(max_digits=12, decimal_places=2)
    module_reference = models.CharField(max_length=32, choices=ModuleCode.choices, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.description} x{self.quantity} ({self.invoice.invoice_number})"
