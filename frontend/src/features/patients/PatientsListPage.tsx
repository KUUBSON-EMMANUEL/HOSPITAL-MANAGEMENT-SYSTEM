import { ResourceListPage } from "@/components/generic/ResourceListPage"
import { patientsResource } from "@/config/clinical-resources"

export function PatientsListPage() {
  return <ResourceListPage config={patientsResource()} />
}
