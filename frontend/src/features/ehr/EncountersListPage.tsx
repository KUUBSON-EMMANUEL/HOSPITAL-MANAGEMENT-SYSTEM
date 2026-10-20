import { ResourceListPage } from "@/components/generic/ResourceListPage"
import { encountersResource } from "@/config/clinical-resources"

export function EncountersListPage() {
  return <ResourceListPage config={encountersResource()} />
}
