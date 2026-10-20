import { createBrowserRouter } from "react-router-dom"

import { AppShell } from "@/components/layout/AppShell"
import { ProtectedRoute } from "@/features/auth/ProtectedRoute"
import { LoginPage } from "@/features/auth/LoginPage"
import { DashboardPage } from "@/features/dashboard/DashboardPage"
import { PatientsListPage } from "@/features/patients/PatientsListPage"
import { PatientDetailPage } from "@/features/patients/PatientDetailPage"
import { AppointmentsListPage } from "@/features/appointments/AppointmentsListPage"
import { EncountersListPage } from "@/features/ehr/EncountersListPage"
import { VitalsListPage } from "@/features/ehr/VitalsListPage"
import { ConsultationsListPage } from "@/features/consultations/ConsultationsListPage"
import { BillingPage } from "@/features/billing/BillingPage"
import { PharmacyPage } from "@/features/pharmacy/PharmacyPage"
import { InventoryPage } from "@/features/inventory/InventoryPage"
import { AuditLogPage } from "@/features/audit/AuditLogPage"
import { ResourceListPage } from "@/components/generic/ResourceListPage"
import {
  branchesResource,
  wardsResource,
  labOrdersResource,
  imagingOrdersResource,
  insurancePoliciesResource,
  staffProfilesResource,
  emergencyCasesResource,
  theatreBookingsResource,
  maternityRecordsResource,
  telemedicineSessionsResource,
  messagesResource,
  notificationsResource,
  reportsResource,
  nursingNotesResource,
} from "@/config/resources"

export const router = createBrowserRouter([
  { path: "/login", element: <LoginPage /> },
  {
    path: "/",
    element: (
      <ProtectedRoute>
        <AppShell />
      </ProtectedRoute>
    ),
    children: [
      { index: true, element: <DashboardPage /> },
      { path: "patients", element: <PatientsListPage /> },
      { path: "patients/:id", element: <PatientDetailPage /> },
      { path: "appointments", element: <AppointmentsListPage /> },
      { path: "ehr/encounters", element: <EncountersListPage /> },
      { path: "ehr/vitals", element: <VitalsListPage /> },
      { path: "consultations", element: <ConsultationsListPage /> },
      { path: "nursing", element: <ResourceListPage config={nursingNotesResource} /> },
      { path: "wards", element: <ResourceListPage config={wardsResource} /> },
      { path: "billing", element: <BillingPage /> },
      { path: "pharmacy", element: <PharmacyPage /> },
      { path: "laboratory", element: <ResourceListPage config={labOrdersResource} /> },
      { path: "radiology", element: <ResourceListPage config={imagingOrdersResource} /> },
      { path: "insurance", element: <ResourceListPage config={insurancePoliciesResource} /> },
      { path: "inventory", element: <InventoryPage /> },
      { path: "staff", element: <ResourceListPage config={staffProfilesResource} /> },
      { path: "branches", element: <ResourceListPage config={branchesResource} /> },
      { path: "emergency", element: <ResourceListPage config={emergencyCasesResource} /> },
      { path: "theatre", element: <ResourceListPage config={theatreBookingsResource} /> },
      { path: "maternity", element: <ResourceListPage config={maternityRecordsResource} /> },
      { path: "telemedicine", element: <ResourceListPage config={telemedicineSessionsResource} /> },
      { path: "messaging", element: <ResourceListPage config={messagesResource} /> },
      { path: "notifications", element: <ResourceListPage config={notificationsResource} /> },
      { path: "reports", element: <ResourceListPage config={reportsResource} /> },
      { path: "audit", element: <AuditLogPage /> },
    ],
  },
])
