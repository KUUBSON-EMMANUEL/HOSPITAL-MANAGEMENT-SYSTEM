from django.contrib import admin

from .models import Invoice, InvoiceLineItem


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ["invoice_number", "patient", "status", "total_amount", "due_date", "branch"]
    list_filter = ["branch", "status"]
    search_fields = ["invoice_number", "patient__first_name", "patient__last_name"]


@admin.register(InvoiceLineItem)
class InvoiceLineItemAdmin(admin.ModelAdmin):
    list_display = ["invoice", "description", "quantity", "unit_price", "line_total", "module_reference"]
    list_filter = ["module_reference"]
    search_fields = ["description", "invoice__invoice_number"]
