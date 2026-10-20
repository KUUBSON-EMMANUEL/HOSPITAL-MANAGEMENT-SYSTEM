import { ResourceListPage } from "@/components/generic/ResourceListPage"
import { vitalsResource } from "@/config/clinical-resources"

export function VitalsListPage() {
  return <ResourceListPage config={vitalsResource()} />
}
