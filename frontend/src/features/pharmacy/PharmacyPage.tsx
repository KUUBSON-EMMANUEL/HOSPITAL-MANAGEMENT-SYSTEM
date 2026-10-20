import { TabbedResourcesPage } from "@/components/generic/TabbedResourcesPage"
import { prescriptionItemsResource, prescriptionsResource } from "@/config/resources"

export function PharmacyPage() {
  return (
    <TabbedResourcesPage
      tabs={[
        { label: "Prescriptions", config: prescriptionsResource },
        { label: "Items", config: prescriptionItemsResource },
      ]}
    />
  )
}
