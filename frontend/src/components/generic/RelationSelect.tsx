import { useQuery } from "@tanstack/react-query"

import { apiClient } from "@/lib/api-client"
import type { RelationConfig } from "@/lib/resource-config"
import type { Paginated } from "@/types/api"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"

export function RelationSelect({
  relation,
  value,
  onChange,
  required,
}: {
  relation: RelationConfig
  value: string
  onChange: (value: string) => void
  required?: boolean
}) {
  const { data, isLoading } = useQuery({
    queryKey: ["relation-options", relation.endpoint],
    queryFn: () =>
      apiClient
        .get<Paginated<Record<string, unknown>>>(relation.endpoint, { params: { page_size: 200 } })
        .then((r) => r.data.results),
  })

  return (
    <Select
      value={value || undefined}
      onValueChange={(v) => onChange(v === "__none__" ? "" : v)}
    >
      <SelectTrigger>
        <SelectValue placeholder={isLoading ? "Loading…" : "Select…"} />
      </SelectTrigger>
      <SelectContent>
        {!required && <SelectItem value="__none__">—</SelectItem>}
        {data?.map((item) => (
          <SelectItem key={item.public_id as string} value={item.public_id as string}>
            {relation.labelFn(item)}
          </SelectItem>
        ))}
      </SelectContent>
    </Select>
  )
}
