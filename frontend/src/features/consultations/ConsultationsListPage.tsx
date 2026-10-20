import { ResourceListPage } from "@/components/generic/ResourceListPage"
import { consultationsResource } from "@/config/clinical-resources"

export function ConsultationsListPage() {
  return <ResourceListPage config={consultationsResource()} />
}
