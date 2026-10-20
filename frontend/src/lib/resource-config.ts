export type FieldType =
  | "text"
  | "textarea"
  | "number"
  | "date"
  | "datetime-local"
  | "select"
  | "checkbox"
  /** Comma-separated text in the UI, stored as a JSON string[] on the wire (e.g. Patient.allergies). */
  | "tags"

export interface RelationConfig {
  /** API endpoint (relative to base URL) to fetch options from, e.g. "/patients/". */
  endpoint: string
  /** Renders the human-readable label for one related item. */
  labelFn: (item: Record<string, unknown>) => string
}

export interface FieldConfig {
  name: string
  label: string
  type: FieldType
  required?: boolean
  /** Static choices, for plain (non-relational) select fields. */
  options?: { value: string; label: string }[]
  /** For FK fields: populates the select from another endpoint instead of static options. */
  relation?: RelationConfig
  /** Show this field in the list table. Defaults to true for non-textarea fields. */
  inList?: boolean
  /** Server-generated field (e.g. patient_number, invoice_number): shown but not editable, never sent on save. */
  readOnly?: boolean
}

export interface ResourceConfig {
  key: string
  label: string
  /** Endpoint relative to the API base, e.g. "/wards/beds/". */
  endpoint: string
  fields: FieldConfig[]
  /** If set, adds a "view" link per row to a bespoke detail page (e.g. patients). */
  getDetailPath?: (row: Record<string, unknown>) => string
  /** Extra query params always applied to the list request, e.g. { patient: id } for a scoped sub-view. */
  extraParams?: Record<string, string>
}
