import { useQuery } from "@tanstack/react-query"
import { isAxiosError } from "axios"

import { apiClient } from "@/lib/api-client"
import type { Paginated } from "@/types/api"
import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"

interface AuditLogEntry {
  public_id: string
  actor: string | null
  actor_email_snapshot: string
  action: string
  severity: "info" | "warning" | "critical"
  request_method: string
  request_path: string
  status_code: number | null
  duration_ms: number | null
  created_at: string
}

export function AuditLogPage() {
  const query = useQuery({
    queryKey: ["audit-log"],
    queryFn: () => apiClient.get<Paginated<AuditLogEntry>>("/audit/").then((r) => r.data),
  })

  if (query.isError) {
    const status = isAxiosError(query.error) ? query.error.response?.status : undefined
    if (status === 403) {
      return (
        <Card className="p-8 text-center text-sm text-muted-foreground">
          You don't have permission to view the audit log.
        </Card>
      )
    }
    return <Card className="p-8 text-center text-sm text-destructive">Failed to load audit log.</Card>
  }

  return (
    <div className="flex flex-col gap-4">
      <h1 className="text-xl font-semibold">Audit Log</h1>
      <Card className="overflow-hidden">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Time</TableHead>
              <TableHead>Actor</TableHead>
              <TableHead>Action</TableHead>
              <TableHead>Method</TableHead>
              <TableHead>Path</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Severity</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {query.isPending && (
              <TableRow>
                <TableCell colSpan={7} className="text-center text-muted-foreground">
                  Loading…
                </TableCell>
              </TableRow>
            )}
            {query.data?.results.map((entry) => (
              <TableRow key={entry.public_id}>
                <TableCell>{new Date(entry.created_at).toLocaleString()}</TableCell>
                <TableCell>{entry.actor_email_snapshot || "system"}</TableCell>
                <TableCell>{entry.action}</TableCell>
                <TableCell>{entry.request_method}</TableCell>
                <TableCell className="max-w-64 truncate">{entry.request_path}</TableCell>
                <TableCell>{entry.status_code}</TableCell>
                <TableCell>
                  <Badge variant={entry.severity === "warning" ? "warning" : entry.severity === "critical" ? "destructive" : "secondary"}>
                    {entry.severity}
                  </Badge>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </Card>
    </div>
  )
}
