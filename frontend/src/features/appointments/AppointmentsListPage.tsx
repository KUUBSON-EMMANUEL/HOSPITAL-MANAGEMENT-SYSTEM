import { ResourceListPage } from "@/components/generic/ResourceListPage"
import { appointmentsResource } from "@/config/clinical-resources"

export function AppointmentsListPage() {
  return <ResourceListPage config={appointmentsResource()} />
}
