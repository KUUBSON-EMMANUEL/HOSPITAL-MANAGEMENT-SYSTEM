import { useParams, Link } from "react-router-dom"
import { useQuery } from "@tanstack/react-query"
import { ArrowLeft } from "lucide-react"

import { apiClient } from "@/lib/api-client"
import type { Patient } from "@/types/api"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { ResourceListPage } from "@/components/generic/ResourceListPage"
import { appointmentsResource, consultationsResource, encountersResource, vitalsResource } from "@/config/clinical-resources"

export function PatientDetailPage() {
  const { id = "" } = useParams()

  const patientQuery = useQuery({
    queryKey: ["patient", id],
    queryFn: () => apiClient.get<Patient>(`/patients/${id}/`).then((r) => r.data),
  })

  if (patientQuery.isPending) {
    return <p className="text-sm text-muted-foreground">Loading…</p>
  }
  if (patientQuery.isError || !patientQuery.data) {
    return <p className="text-sm text-destructive">Patient not found.</p>
  }

  const patient = patientQuery.data
  const age = calculateAge(patient.date_of_birth)

  return (
    <div className="flex flex-col gap-4">
      <Button variant="ghost" size="sm" asChild className="w-fit">
        <Link to="/patients">
          <ArrowLeft /> Back to patients
        </Link>
      </Button>

      <Card>
        <CardHeader>
          <CardTitle className="flex flex-wrap items-center gap-2">
            {patient.first_name} {patient.last_name}
            <Badge variant="secondary">{patient.patient_number}</Badge>
          </CardTitle>
        </CardHeader>
        <CardContent className="grid grid-cols-2 gap-x-6 gap-y-2 text-sm sm:grid-cols-4">
          <Field label="Sex" value={patient.sex} />
          <Field label="Age" value={`${age}`} />
          <Field label="Blood Type" value={patient.blood_type || "—"} />
          <Field label="Phone" value={patient.phone_number || "—"} />
          <Field label="Email" value={patient.email || "—"} />
          <Field label="City" value={patient.city || "—"} />
          <Field
            label="Emergency Contact"
            value={patient.emergency_contact_name ? `${patient.emergency_contact_name} (${patient.emergency_contact_phone})` : "—"}
          />
          <Field label="Allergies" value={patient.allergies.length ? patient.allergies.join(", ") : "None recorded"} />
        </CardContent>
      </Card>

      <Tabs defaultValue="appointments">
        <TabsList>
          <TabsTrigger value="appointments">Appointments</TabsTrigger>
          <TabsTrigger value="encounters">Encounters</TabsTrigger>
          <TabsTrigger value="vitals">Vital Signs</TabsTrigger>
          <TabsTrigger value="consultations">Consultations</TabsTrigger>
        </TabsList>
        <TabsContent value="appointments">
          <ResourceListPage config={appointmentsResource({ patient: patient.public_id })} />
        </TabsContent>
        <TabsContent value="encounters">
          <ResourceListPage config={encountersResource({ patient: patient.public_id })} />
        </TabsContent>
        <TabsContent value="vitals">
          <ResourceListPage config={vitalsResource({ patient: patient.public_id })} />
        </TabsContent>
        <TabsContent value="consultations">
          <ResourceListPage config={consultationsResource({ patient: patient.public_id })} />
        </TabsContent>
      </Tabs>
    </div>
  )
}

function Field({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <p className="text-xs text-muted-foreground">{label}</p>
      <p>{value}</p>
    </div>
  )
}

function calculateAge(dob: string): number {
  const birth = new Date(dob)
  const now = new Date()
  let age = now.getFullYear() - birth.getFullYear()
  const monthDiff = now.getMonth() - birth.getMonth()
  if (monthDiff < 0 || (monthDiff === 0 && now.getDate() < birth.getDate())) age--
  return age
}
