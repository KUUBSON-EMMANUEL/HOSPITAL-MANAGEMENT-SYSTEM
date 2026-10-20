import type { ResourceConfig } from "@/lib/resource-config"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { ResourceListPage } from "./ResourceListPage"

export function TabbedResourcesPage({ tabs }: { tabs: { label: string; config: ResourceConfig }[] }) {
  return (
    <Tabs defaultValue={tabs[0].config.key}>
      <TabsList>
        {tabs.map((t) => (
          <TabsTrigger key={t.config.key} value={t.config.key}>
            {t.label}
          </TabsTrigger>
        ))}
      </TabsList>
      {tabs.map((t) => (
        <TabsContent key={t.config.key} value={t.config.key}>
          <ResourceListPage config={t.config} />
        </TabsContent>
      ))}
    </Tabs>
  )
}
