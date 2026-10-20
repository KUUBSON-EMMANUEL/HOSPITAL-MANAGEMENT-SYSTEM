import { TabbedResourcesPage } from "@/components/generic/TabbedResourcesPage"
import { inventoryItemsResource, stockMovementsResource } from "@/config/resources"

export function InventoryPage() {
  return (
    <TabbedResourcesPage
      tabs={[
        { label: "Items", config: inventoryItemsResource },
        { label: "Movements", config: stockMovementsResource },
      ]}
    />
  )
}
