from rest_framework import serializers

from apps.branches.models import Branch
from apps.core.serializers import PublicIdRelatedField
from apps.patients.models import Patient

from .models import Invoice, InvoiceLineItem, generate_invoice_number


class InvoiceSerializer(serializers.ModelSerializer):
    branch = PublicIdRelatedField(queryset=Branch.objects.all())
    patient = PublicIdRelatedField(queryset=Patient.objects.all())

    class Meta:
        model = Invoice
        fields = [
            "public_id", "branch", "patient", "invoice_number", "status",
            "subtotal", "tax_amount", "discount_amount", "total_amount",
            "due_date", "issued_at", "created_at", "updated_at",
        ]
        read_only_fields = ["public_id", "invoice_number", "created_at", "updated_at"]

    def create(self, validated_data):
        validated_data["invoice_number"] = generate_invoice_number(validated_data["branch"])
        return super().create(validated_data)


class InvoiceLineItemSerializer(serializers.ModelSerializer):
    invoice = PublicIdRelatedField(queryset=Invoice.objects.all())

    class Meta:
        model = InvoiceLineItem
        fields = [
            "public_id", "invoice", "description", "quantity", "unit_price", "line_total",
            "module_reference", "created_at", "updated_at",
        ]
        read_only_fields = ["public_id", "created_at", "updated_at"]
