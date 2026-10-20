export interface Paginated<T> {
  count: number
  total_pages: number
  current_page: number
  next: string | null
  previous: string | null
  results: T[]
}

export interface Branch {
  public_id: string
  code: string
  name: string
  is_main_branch: boolean
  is_active: boolean
  address_line1: string
  address_line2: string
  city: string
  state_region: string
  country: string
  postal_code: string
  phone_number: string
  email: string
  timezone: string
  license_number: string
  bed_capacity: number
  created_at: string
  updated_at: string
}

export interface UserProfile {
  public_id: string
  email: string
  first_name: string
  last_name: string
  phone_number: string
  employee_id: string | null
  branch: string | null
  roles: string[]
  is_active: boolean
  is_staff: boolean
  must_change_password: boolean
  mfa_enabled: boolean
  created_at: string
  updated_at: string
}

export interface Patient {
  public_id: string
  patient_number: string
  branch: string
  first_name: string
  last_name: string
  middle_name: string
  date_of_birth: string
  sex: "M" | "F" | "O"
  blood_type: string
  phone_number: string
  email: string
  address_line1: string
  address_line2: string
  city: string
  state_region: string
  country: string
  emergency_contact_name: string
  emergency_contact_phone: string
  emergency_contact_relationship: string
  allergies: string[]
  registration_date: string
  created_at: string
  updated_at: string
}

export type AppointmentStatus =
  | "scheduled"
  | "confirmed"
  | "checked_in"
  | "in_progress"
  | "completed"
  | "cancelled"
  | "no_show"

export interface Appointment {
  public_id: string
  branch: string
  patient: string
  provider: string
  module: string
  appointment_type: "new_visit" | "follow_up" | "procedure" | "consultation"
  scheduled_start: string
  scheduled_end: string
  status: AppointmentStatus
  reason: string
  cancellation_reason: string
  created_at: string
  updated_at: string
}

export interface Encounter {
  public_id: string
  branch: string
  patient: string
  appointment: string | null
  attending_provider: string
  encounter_type: "outpatient" | "inpatient" | "emergency" | "telemedicine"
  status: "open" | "closed"
  started_at: string
  ended_at: string | null
  chief_complaint: string
  created_at: string
  updated_at: string
}

export interface VitalSigns {
  public_id: string
  branch: string
  patient: string
  encounter: string | null
  recorded_by: string
  recorded_at: string
  temperature_celsius: string | null
  pulse_bpm: number | null
  respiratory_rate: number | null
  systolic_bp: number | null
  diastolic_bp: number | null
  spo2_percent: number | null
  weight_kg: string | null
  height_cm: string | null
  created_at: string
  updated_at: string
}

export interface Diagnosis {
  code: string
  description: string
}

export interface Consultation {
  public_id: string
  branch: string
  patient: string
  provider: string
  appointment: string | null
  encounter: string | null
  chief_complaint: string
  subjective: string
  objective: string
  assessment: string
  plan: string
  diagnosis: Diagnosis[]
  status: "in_progress" | "completed" | "cancelled"
  created_at: string
  updated_at: string
}
