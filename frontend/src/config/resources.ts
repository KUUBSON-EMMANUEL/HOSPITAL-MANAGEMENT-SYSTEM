import type { ResourceConfig, RelationConfig } from "@/lib/resource-config"

const branchRelation: RelationConfig = {
  endpoint: "/branches/",
  labelFn: (i) => `${i.name as string} (${i.code as string})`,
}

const patientRelation: RelationConfig = {
  endpoint: "/patients/",
  labelFn: (i) => `${i.patient_number as string} — ${i.first_name as string} ${i.last_name as string}`,
}

const userRelation: RelationConfig = {
  endpoint: "/auth/users/",
  labelFn: (i) => `${i.first_name as string} ${i.last_name as string} (${i.email as string})`,
}

const encounterRelation: RelationConfig = {
  endpoint: "/ehr/encounters/",
  labelFn: (i) => `${i.encounter_type as string} — ${(i.started_at as string)?.slice(0, 10)}`,
}

const invoiceRelation: RelationConfig = {
  endpoint: "/billing/invoices/",
  labelFn: (i) => i.invoice_number as string,
}

const prescriptionRelation: RelationConfig = {
  endpoint: "/pharmacy/prescriptions/",
  labelFn: (i) => `Prescription (${(i.created_at as string)?.slice(0, 10)})`,
}

const inventoryItemRelation: RelationConfig = {
  endpoint: "/inventory/items/",
  labelFn: (i) => `${i.name as string} (${i.sku as string})`,
}

export const branchesResource: ResourceConfig = {
  key: "branches",
  label: "Branches",
  endpoint: "/branches/",
  fields: [
    { name: "code", label: "Code", type: "text", required: true },
    { name: "name", label: "Name", type: "text", required: true },
    { name: "city", label: "City", type: "text" },
    { name: "country", label: "Country", type: "text" },
    { name: "phone_number", label: "Phone", type: "text" },
    { name: "bed_capacity", label: "Bed Capacity", type: "number" },
    { name: "is_active", label: "Active", type: "checkbox" },
    { name: "is_main_branch", label: "Main Branch", type: "checkbox" },
    { name: "address_line1", label: "Address", type: "text", inList: false },
    { name: "state_region", label: "State/Region", type: "text", inList: false },
  ],
}

export const wardsResource: ResourceConfig = {
  key: "wards",
  label: "Wards & Beds",
  endpoint: "/wards/beds/",
  fields: [
    { name: "branch", label: "Branch", type: "select", relation: branchRelation, required: true },
    { name: "ward_name", label: "Ward", type: "text", required: true },
    { name: "bed_number", label: "Bed #", type: "text", required: true },
    {
      name: "bed_type",
      label: "Type",
      type: "select",
      required: true,
      options: [
        { value: "general", label: "General" },
        { value: "private", label: "Private" },
        { value: "icu", label: "ICU" },
        { value: "isolation", label: "Isolation" },
      ],
    },
    {
      name: "status",
      label: "Status",
      type: "select",
      options: [
        { value: "available", label: "Available" },
        { value: "occupied", label: "Occupied" },
        { value: "maintenance", label: "Maintenance" },
        { value: "reserved", label: "Reserved" },
      ],
    },
    { name: "current_patient", label: "Current Patient", type: "select", relation: patientRelation },
  ],
}

export const invoicesResource: ResourceConfig = {
  key: "invoices",
  label: "Invoices",
  endpoint: "/billing/invoices/",
  fields: [
    { name: "invoice_number", label: "Invoice #", type: "text", readOnly: true },
    { name: "branch", label: "Branch", type: "select", relation: branchRelation, required: true },
    { name: "patient", label: "Patient", type: "select", relation: patientRelation, required: true },
    {
      name: "status",
      label: "Status",
      type: "select",
      options: [
        { value: "draft", label: "Draft" },
        { value: "issued", label: "Issued" },
        { value: "partially_paid", label: "Partially Paid" },
        { value: "paid", label: "Paid" },
        { value: "void", label: "Void" },
      ],
    },
    { name: "subtotal", label: "Subtotal", type: "number" },
    { name: "tax_amount", label: "Tax", type: "number" },
    { name: "discount_amount", label: "Discount", type: "number" },
    { name: "total_amount", label: "Total", type: "number" },
    { name: "due_date", label: "Due Date", type: "date" },
  ],
}

export const invoiceLineItemsResource: ResourceConfig = {
  key: "invoice-line-items",
  label: "Invoice Line Items",
  endpoint: "/billing/line-items/",
  fields: [
    { name: "invoice", label: "Invoice", type: "select", relation: invoiceRelation, required: true },
    { name: "description", label: "Description", type: "text", required: true },
    { name: "quantity", label: "Qty", type: "number", required: true },
    { name: "unit_price", label: "Unit Price", type: "number", required: true },
    { name: "line_total", label: "Line Total", type: "number", required: true },
  ],
}

export const prescriptionsResource: ResourceConfig = {
  key: "prescriptions",
  label: "Prescriptions",
  endpoint: "/pharmacy/prescriptions/",
  fields: [
    { name: "branch", label: "Branch", type: "select", relation: branchRelation, required: true },
    { name: "patient", label: "Patient", type: "select", relation: patientRelation, required: true },
    { name: "prescriber", label: "Prescriber", type: "select", relation: userRelation, required: true },
    {
      name: "status",
      label: "Status",
      type: "select",
      options: [
        { value: "pending", label: "Pending" },
        { value: "dispensed", label: "Dispensed" },
        { value: "partially_dispensed", label: "Partially Dispensed" },
        { value: "cancelled", label: "Cancelled" },
      ],
    },
    { name: "notes", label: "Notes", type: "textarea" },
  ],
}

export const prescriptionItemsResource: ResourceConfig = {
  key: "prescription-items",
  label: "Prescription Items",
  endpoint: "/pharmacy/items/",
  fields: [
    { name: "prescription", label: "Prescription", type: "select", relation: prescriptionRelation, required: true },
    { name: "drug_name", label: "Drug", type: "text", required: true },
    { name: "dosage", label: "Dosage", type: "text", required: true },
    { name: "frequency", label: "Frequency", type: "text", required: true },
    { name: "duration", label: "Duration", type: "text", required: true },
    { name: "quantity", label: "Quantity", type: "number", required: true },
  ],
}

export const labOrdersResource: ResourceConfig = {
  key: "lab-orders",
  label: "Laboratory Orders",
  endpoint: "/laboratory/orders/",
  fields: [
    { name: "branch", label: "Branch", type: "select", relation: branchRelation, required: true },
    { name: "patient", label: "Patient", type: "select", relation: patientRelation, required: true },
    { name: "ordering_provider", label: "Ordering Provider", type: "select", relation: userRelation, required: true },
    { name: "test_name", label: "Test", type: "text", required: true },
    {
      name: "status",
      label: "Status",
      type: "select",
      options: [
        { value: "ordered", label: "Ordered" },
        { value: "collected", label: "Collected" },
        { value: "in_progress", label: "In Progress" },
        { value: "completed", label: "Completed" },
        { value: "cancelled", label: "Cancelled" },
      ],
    },
    { name: "result_value", label: "Result", type: "text" },
    { name: "reference_range", label: "Reference Range", type: "text" },
    { name: "result_text", label: "Result Notes", type: "textarea" },
  ],
}

export const imagingOrdersResource: ResourceConfig = {
  key: "imaging-orders",
  label: "Radiology Orders",
  endpoint: "/radiology/orders/",
  fields: [
    { name: "branch", label: "Branch", type: "select", relation: branchRelation, required: true },
    { name: "patient", label: "Patient", type: "select", relation: patientRelation, required: true },
    { name: "ordering_provider", label: "Ordering Provider", type: "select", relation: userRelation, required: true },
    {
      name: "modality",
      label: "Modality",
      type: "select",
      required: true,
      options: [
        { value: "xray", label: "X-Ray" },
        { value: "ct", label: "CT" },
        { value: "mri", label: "MRI" },
        { value: "ultrasound", label: "Ultrasound" },
      ],
    },
    {
      name: "status",
      label: "Status",
      type: "select",
      options: [
        { value: "ordered", label: "Ordered" },
        { value: "scheduled", label: "Scheduled" },
        { value: "in_progress", label: "In Progress" },
        { value: "completed", label: "Completed" },
        { value: "cancelled", label: "Cancelled" },
      ],
    },
    { name: "findings", label: "Findings", type: "textarea" },
    { name: "report", label: "Report", type: "textarea" },
  ],
}

export const insurancePoliciesResource: ResourceConfig = {
  key: "insurance-policies",
  label: "Insurance Policies",
  endpoint: "/insurance/policies/",
  fields: [
    { name: "branch", label: "Branch", type: "select", relation: branchRelation, required: true },
    { name: "patient", label: "Patient", type: "select", relation: patientRelation, required: true },
    { name: "provider_name", label: "Provider", type: "text", required: true },
    { name: "policy_number", label: "Policy #", type: "text", required: true },
    { name: "coverage_type", label: "Coverage", type: "text" },
    { name: "valid_from", label: "Valid From", type: "date", required: true },
    { name: "valid_to", label: "Valid To", type: "date", required: true },
    {
      name: "status",
      label: "Status",
      type: "select",
      options: [
        { value: "active", label: "Active" },
        { value: "expired", label: "Expired" },
        { value: "cancelled", label: "Cancelled" },
      ],
    },
  ],
}

export const inventoryItemsResource: ResourceConfig = {
  key: "inventory-items",
  label: "Inventory Items",
  endpoint: "/inventory/items/",
  fields: [
    { name: "branch", label: "Branch", type: "select", relation: branchRelation, required: true },
    { name: "name", label: "Name", type: "text", required: true },
    { name: "sku", label: "SKU", type: "text", required: true },
    { name: "unit", label: "Unit", type: "text", required: true },
    { name: "quantity_on_hand", label: "On Hand", type: "number" },
    { name: "reorder_level", label: "Reorder Level", type: "number" },
  ],
}

export const stockMovementsResource: ResourceConfig = {
  key: "stock-movements",
  label: "Stock Movements",
  endpoint: "/inventory/movements/",
  fields: [
    { name: "item", label: "Item", type: "select", relation: inventoryItemRelation, required: true },
    {
      name: "movement_type",
      label: "Type",
      type: "select",
      required: true,
      options: [
        { value: "inbound", label: "Inbound" },
        { value: "outbound", label: "Outbound" },
        { value: "adjustment", label: "Adjustment" },
      ],
    },
    { name: "quantity", label: "Quantity", type: "number", required: true },
    { name: "recorded_by", label: "Recorded By", type: "select", relation: userRelation, required: true },
    { name: "reason", label: "Reason", type: "text" },
  ],
}

export const staffProfilesResource: ResourceConfig = {
  key: "staff-profiles",
  label: "Staff Profiles",
  endpoint: "/staff/profiles/",
  fields: [
    { name: "user", label: "User", type: "select", relation: userRelation, required: true },
    { name: "department", label: "Department", type: "text" },
    { name: "designation", label: "Designation", type: "text" },
    { name: "hire_date", label: "Hire Date", type: "date" },
    {
      name: "employment_status",
      label: "Status",
      type: "select",
      options: [
        { value: "active", label: "Active" },
        { value: "on_leave", label: "On Leave" },
        { value: "terminated", label: "Terminated" },
      ],
    },
  ],
}

export const emergencyCasesResource: ResourceConfig = {
  key: "emergency-cases",
  label: "Emergency Cases",
  endpoint: "/emergency/cases/",
  fields: [
    { name: "branch", label: "Branch", type: "select", relation: branchRelation, required: true },
    { name: "patient", label: "Patient", type: "select", relation: patientRelation, required: true },
    {
      name: "triage_level",
      label: "Triage Level",
      type: "select",
      required: true,
      options: [
        { value: "1", label: "1 — Resuscitation" },
        { value: "2", label: "2 — Emergent" },
        { value: "3", label: "3 — Urgent" },
        { value: "4", label: "4 — Less Urgent" },
        { value: "5", label: "5 — Non-Urgent" },
      ],
    },
    {
      name: "status",
      label: "Status",
      type: "select",
      options: [
        { value: "waiting", label: "Waiting" },
        { value: "in_treatment", label: "In Treatment" },
        { value: "admitted", label: "Admitted" },
        { value: "discharged", label: "Discharged" },
        { value: "transferred", label: "Transferred" },
      ],
    },
    { name: "attending_provider", label: "Attending Provider", type: "select", relation: userRelation },
    { name: "chief_complaint", label: "Chief Complaint", type: "textarea" },
  ],
}

export const theatreBookingsResource: ResourceConfig = {
  key: "theatre-bookings",
  label: "Theatre Bookings",
  endpoint: "/theatre/bookings/",
  fields: [
    { name: "branch", label: "Branch", type: "select", relation: branchRelation, required: true },
    { name: "patient", label: "Patient", type: "select", relation: patientRelation, required: true },
    { name: "surgeon", label: "Surgeon", type: "select", relation: userRelation, required: true },
    { name: "procedure_name", label: "Procedure", type: "text", required: true },
    { name: "scheduled_start", label: "Start", type: "datetime-local", required: true },
    { name: "scheduled_end", label: "End", type: "datetime-local", required: true },
    {
      name: "status",
      label: "Status",
      type: "select",
      options: [
        { value: "scheduled", label: "Scheduled" },
        { value: "in_progress", label: "In Progress" },
        { value: "completed", label: "Completed" },
        { value: "cancelled", label: "Cancelled" },
      ],
    },
    { name: "notes", label: "Notes", type: "textarea" },
  ],
}

export const maternityRecordsResource: ResourceConfig = {
  key: "maternity-records",
  label: "Maternity Records",
  endpoint: "/maternity/records/",
  fields: [
    { name: "branch", label: "Branch", type: "select", relation: branchRelation, required: true },
    { name: "patient", label: "Patient", type: "select", relation: patientRelation, required: true },
    { name: "attending_provider", label: "Attending Provider", type: "select", relation: userRelation, required: true },
    { name: "expected_delivery_date", label: "Expected Delivery", type: "date" },
    {
      name: "status",
      label: "Status",
      type: "select",
      options: [
        { value: "antenatal", label: "Antenatal" },
        { value: "delivered", label: "Delivered" },
        { value: "postnatal", label: "Postnatal" },
      ],
    },
    { name: "notes", label: "Notes", type: "textarea" },
  ],
}

export const telemedicineSessionsResource: ResourceConfig = {
  key: "telemedicine-sessions",
  label: "Telemedicine Sessions",
  endpoint: "/telemedicine/sessions/",
  fields: [
    { name: "branch", label: "Branch", type: "select", relation: branchRelation, required: true },
    { name: "patient", label: "Patient", type: "select", relation: patientRelation, required: true },
    { name: "provider", label: "Provider", type: "select", relation: userRelation, required: true },
    { name: "scheduled_start", label: "Start", type: "datetime-local", required: true },
    { name: "scheduled_end", label: "End", type: "datetime-local", required: true },
    {
      name: "status",
      label: "Status",
      type: "select",
      options: [
        { value: "scheduled", label: "Scheduled" },
        { value: "in_progress", label: "In Progress" },
        { value: "completed", label: "Completed" },
        { value: "cancelled", label: "Cancelled" },
      ],
    },
    { name: "session_url", label: "Session URL", type: "text" },
  ],
}

export const messagesResource: ResourceConfig = {
  key: "messages",
  label: "Messages",
  endpoint: "/messaging/messages/",
  fields: [
    { name: "sender", label: "Sender", type: "select", relation: userRelation, required: true },
    { name: "recipient", label: "Recipient", type: "select", relation: userRelation, required: true },
    { name: "body", label: "Message", type: "textarea", required: true },
  ],
}

export const notificationsResource: ResourceConfig = {
  key: "notifications",
  label: "Notifications",
  endpoint: "/notifications/",
  fields: [
    { name: "recipient", label: "Recipient", type: "select", relation: userRelation, required: true },
    { name: "title", label: "Title", type: "text", required: true },
    {
      name: "channel",
      label: "Channel",
      type: "select",
      options: [
        { value: "in_app", label: "In-App" },
        { value: "email", label: "Email" },
        { value: "sms", label: "SMS" },
      ],
    },
    {
      name: "status",
      label: "Status",
      type: "select",
      options: [
        { value: "pending", label: "Pending" },
        { value: "sent", label: "Sent" },
        { value: "failed", label: "Failed" },
        { value: "read", label: "Read" },
      ],
    },
    { name: "body", label: "Body", type: "textarea" },
  ],
}

export const reportsResource: ResourceConfig = {
  key: "reports",
  label: "Saved Reports",
  endpoint: "/reports/",
  fields: [
    { name: "branch", label: "Branch", type: "select", relation: branchRelation, required: true },
    { name: "name", label: "Name", type: "text", required: true },
    { name: "report_type", label: "Type", type: "text", required: true },
    { name: "generated_by", label: "Generated By", type: "select", relation: userRelation },
  ],
}

export const nursingNotesResource: ResourceConfig = {
  key: "nursing-notes",
  label: "Nursing Notes",
  endpoint: "/nursing/notes/",
  fields: [
    { name: "branch", label: "Branch", type: "select", relation: branchRelation, required: true },
    { name: "patient", label: "Patient", type: "select", relation: patientRelation, required: true },
    { name: "encounter", label: "Encounter", type: "select", relation: encounterRelation },
    { name: "nurse", label: "Nurse", type: "select", relation: userRelation, required: true },
    {
      name: "shift",
      label: "Shift",
      type: "select",
      required: true,
      options: [
        { value: "morning", label: "Morning" },
        { value: "afternoon", label: "Afternoon" },
        { value: "night", label: "Night" },
      ],
    },
    { name: "note", label: "Note", type: "textarea", required: true },
  ],
}
