import type { ResourceConfig, RelationConfig } from "@/lib/resource-config"

export const branchRelation: RelationConfig = {
  endpoint: "/branches/",
  labelFn: (i) => `${i.name as string} (${i.code as string})`,
}

export const patientRelation: RelationConfig = {
  endpoint: "/patients/",
  labelFn: (i) => `${i.patient_number as string} — ${i.first_name as string} ${i.last_name as string}`,
}

export const userRelation: RelationConfig = {
  endpoint: "/auth/users/",
  labelFn: (i) => `${i.first_name as string} ${i.last_name as string} (${i.email as string})`,
}

export const appointmentRelation: RelationConfig = {
  endpoint: "/appointments/",
  labelFn: (i) => `Appointment — ${(i.scheduled_start as string)?.slice(0, 16).replace("T", " ")}`,
}

export const encounterRelation: RelationConfig = {
  endpoint: "/ehr/encounters/",
  labelFn: (i) => `${i.encounter_type as string} — ${(i.started_at as string)?.slice(0, 10)}`,
}

export function patientsResource(): ResourceConfig {
  return {
    key: "patients",
    label: "Patients",
    endpoint: "/patients/",
    getDetailPath: (row) => `/patients/${row.public_id as string}`,
    fields: [
      { name: "patient_number", label: "MRN", type: "text", readOnly: true },
      { name: "branch", label: "Branch", type: "select", relation: branchRelation, required: true },
      { name: "first_name", label: "First Name", type: "text", required: true },
      { name: "last_name", label: "Last Name", type: "text", required: true },
      { name: "middle_name", label: "Middle Name", type: "text", inList: false },
      { name: "date_of_birth", label: "Date of Birth", type: "date", required: true },
      {
        name: "sex",
        label: "Sex",
        type: "select",
        required: true,
        options: [
          { value: "M", label: "Male" },
          { value: "F", label: "Female" },
          { value: "O", label: "Other" },
        ],
      },
      {
        name: "blood_type",
        label: "Blood Type",
        type: "select",
        options: ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-", "unknown"].map((v) => ({
          value: v,
          label: v === "unknown" ? "Unknown" : v,
        })),
      },
      { name: "phone_number", label: "Phone", type: "text" },
      { name: "email", label: "Email", type: "text", inList: false },
      { name: "city", label: "City", type: "text", inList: false },
      { name: "country", label: "Country", type: "text", inList: false },
      { name: "emergency_contact_name", label: "Emergency Contact", type: "text", inList: false },
      { name: "emergency_contact_phone", label: "Emergency Phone", type: "text", inList: false },
      { name: "allergies", label: "Allergies", type: "tags", inList: false },
    ],
  }
}

export function appointmentsResource(extraParams?: Record<string, string>): ResourceConfig {
  return {
    key: "appointments",
    label: "Appointments",
    endpoint: "/appointments/",
    extraParams,
    fields: [
      { name: "branch", label: "Branch", type: "select", relation: branchRelation, required: true },
      { name: "patient", label: "Patient", type: "select", relation: patientRelation, required: true },
      { name: "provider", label: "Provider", type: "select", relation: userRelation, required: true },
      {
        name: "appointment_type",
        label: "Type",
        type: "select",
        required: true,
        options: [
          { value: "new_visit", label: "New Visit" },
          { value: "follow_up", label: "Follow-up" },
          { value: "procedure", label: "Procedure" },
          { value: "consultation", label: "Consultation" },
        ],
      },
      { name: "scheduled_start", label: "Start", type: "datetime-local", required: true },
      { name: "scheduled_end", label: "End", type: "datetime-local", required: true },
      {
        name: "status",
        label: "Status",
        type: "select",
        options: [
          { value: "scheduled", label: "Scheduled" },
          { value: "confirmed", label: "Confirmed" },
          { value: "checked_in", label: "Checked In" },
          { value: "in_progress", label: "In Progress" },
          { value: "completed", label: "Completed" },
          { value: "cancelled", label: "Cancelled" },
          { value: "no_show", label: "No Show" },
        ],
      },
      { name: "reason", label: "Reason", type: "textarea" },
    ],
  }
}

export function encountersResource(extraParams?: Record<string, string>): ResourceConfig {
  return {
    key: "encounters",
    label: "Encounters",
    endpoint: "/ehr/encounters/",
    extraParams,
    fields: [
      { name: "branch", label: "Branch", type: "select", relation: branchRelation, required: true },
      { name: "patient", label: "Patient", type: "select", relation: patientRelation, required: true },
      { name: "appointment", label: "Appointment", type: "select", relation: appointmentRelation },
      { name: "attending_provider", label: "Attending Provider", type: "select", relation: userRelation, required: true },
      {
        name: "encounter_type",
        label: "Type",
        type: "select",
        required: true,
        options: [
          { value: "outpatient", label: "Outpatient" },
          { value: "inpatient", label: "Inpatient" },
          { value: "emergency", label: "Emergency" },
          { value: "telemedicine", label: "Telemedicine" },
        ],
      },
      {
        name: "status",
        label: "Status",
        type: "select",
        options: [
          { value: "open", label: "Open" },
          { value: "closed", label: "Closed" },
        ],
      },
      { name: "chief_complaint", label: "Chief Complaint", type: "textarea" },
    ],
  }
}

export function vitalsResource(extraParams?: Record<string, string>): ResourceConfig {
  return {
    key: "vitals",
    label: "Vital Signs",
    endpoint: "/ehr/vitals/",
    extraParams,
    fields: [
      { name: "branch", label: "Branch", type: "select", relation: branchRelation, required: true },
      { name: "patient", label: "Patient", type: "select", relation: patientRelation, required: true },
      { name: "encounter", label: "Encounter", type: "select", relation: encounterRelation },
      { name: "recorded_by", label: "Recorded By", type: "select", relation: userRelation, required: true },
      { name: "temperature_celsius", label: "Temp (°C)", type: "number" },
      { name: "pulse_bpm", label: "Pulse (bpm)", type: "number" },
      { name: "respiratory_rate", label: "Resp. Rate", type: "number" },
      { name: "systolic_bp", label: "Systolic BP", type: "number" },
      { name: "diastolic_bp", label: "Diastolic BP", type: "number" },
      { name: "spo2_percent", label: "SpO2 (%)", type: "number" },
      { name: "weight_kg", label: "Weight (kg)", type: "number" },
      { name: "height_cm", label: "Height (cm)", type: "number" },
    ],
  }
}

export function consultationsResource(extraParams?: Record<string, string>): ResourceConfig {
  return {
    key: "consultations",
    label: "Consultations",
    endpoint: "/consultations/",
    extraParams,
    fields: [
      { name: "branch", label: "Branch", type: "select", relation: branchRelation, required: true },
      { name: "patient", label: "Patient", type: "select", relation: patientRelation, required: true },
      { name: "provider", label: "Provider", type: "select", relation: userRelation, required: true },
      { name: "appointment", label: "Appointment", type: "select", relation: appointmentRelation },
      { name: "encounter", label: "Encounter", type: "select", relation: encounterRelation },
      {
        name: "status",
        label: "Status",
        type: "select",
        options: [
          { value: "in_progress", label: "In Progress" },
          { value: "completed", label: "Completed" },
          { value: "cancelled", label: "Cancelled" },
        ],
      },
      { name: "chief_complaint", label: "Chief Complaint", type: "textarea" },
      { name: "subjective", label: "Subjective", type: "textarea", inList: false },
      { name: "objective", label: "Objective", type: "textarea", inList: false },
      { name: "assessment", label: "Assessment", type: "textarea", inList: false },
      { name: "plan", label: "Plan", type: "textarea", inList: false },
      // diagnosis (structured ICD-style list) isn't edited through this generic
      // form pass -- it's a JSON list of {code, description}, which the
      // generic FieldConfig types don't model yet. Visible/editable via the
      // API or admin; a dedicated diagnosis editor is a follow-up.
    ],
  }
}
