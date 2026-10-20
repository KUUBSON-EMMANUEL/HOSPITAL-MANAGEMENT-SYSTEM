import { TabbedResourcesPage } from "@/components/generic/TabbedResourcesPage"
import { invoiceLineItemsResource, invoicesResource } from "@/config/resources"

export function BillingPage() {
  return (
    <TabbedResourcesPage
      tabs={[
        { label: "Invoices", config: invoicesResource },
        { label: "Line Items", config: invoiceLineItemsResource },
      ]}
    />
  )
}
