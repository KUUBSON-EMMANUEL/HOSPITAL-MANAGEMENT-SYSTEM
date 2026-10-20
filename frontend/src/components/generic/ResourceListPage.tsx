import * as React from "react"
import { useMutation, useQueries, useQuery, useQueryClient } from "@tanstack/react-query"
import { isAxiosError } from "axios"
import { Eye, Pencil, Plus, Trash2 } from "lucide-react"
import { Link } from "react-router-dom"

import { apiClient } from "@/lib/api-client"
import type { FieldConfig, ResourceConfig } from "@/lib/resource-config"
import type { Paginated } from "@/types/api"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import {
  Dialog,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { ResourceForm, type FormValues } from "./ResourceForm"

type Row = Record<string, unknown>

export function ResourceListPage({ config }: { config: ResourceConfig }) {
  const queryClient = useQueryClient()
  const [dialogRow, setDialogRow] = React.useState<Row | null | undefined>(undefined) // undefined = closed, null = create
  const [formValues, setFormValues] = React.useState<FormValues>({})
  const [formError, setFormError] = React.useState<string | null>(null)

  const listQuery = useQuery({
    queryKey: ["resource", config.key, config.extraParams],
    queryFn: () =>
      apiClient.get<Paginated<Row>>(config.endpoint, { params: config.extraParams }).then((r) => r.data),
  })

  const saveMutation = useMutation({
    mutationFn: (values: FormValues) => {
      const payload = cleanPayload(values, config.fields)
      if (dialogRow) {
        return apiClient.patch(`${config.endpoint}${dialogRow.public_id}/`, payload)
      }
      return apiClient.post(config.endpoint, payload)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["resource", config.key] })
      setDialogRow(undefined)
    },
    onError: (err) => setFormError(extractError(err)),
  })

  const deleteMutation = useMutation({
    mutationFn: (row: Row) => apiClient.delete(`${config.endpoint}${row.public_id}/`),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["resource", config.key] }),
  })

  function openCreate() {
    setFormError(null)
    setFormValues({})
    setDialogRow(null)
  }

  function openEdit(row: Row) {
    setFormError(null)
    const initial: FormValues = {}
    for (const field of config.fields) {
      if (field.type === "tags") {
        initial[field.name] = Array.isArray(row[field.name]) ? (row[field.name] as string[]).join(", ") : ""
        continue
      }
      initial[field.name] = (row[field.name] as string | boolean) ?? (field.type === "checkbox" ? false : "")
    }
    setFormValues(initial)
    setDialogRow(row)
  }

  const listColumns = config.fields.filter((f) => f.inList !== false && f.type !== "textarea").slice(0, 6)
  const relationLabels = useRelationLabelMaps(listColumns)

  if (listQuery.isError) {
    const status = isAxiosError(listQuery.error) ? listQuery.error.response?.status : undefined
    if (status === 403) {
      return (
        <Card className="p-8 text-center text-sm text-muted-foreground">
          You don't have permission to view {config.label}.
        </Card>
      )
    }
    return (
      <Card className="p-8 text-center text-sm text-destructive">Failed to load {config.label}.</Card>
    )
  }

  return (
    <div className="flex flex-col gap-4">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-semibold">{config.label}</h1>
        <Button onClick={openCreate} size="sm">
          <Plus /> New
        </Button>
      </div>

      <Card className="overflow-hidden">
        <Table>
          <TableHeader>
            <TableRow>
              {listColumns.map((f) => (
                <TableHead key={f.name}>{f.label}</TableHead>
              ))}
              <TableHead className="w-20" />
            </TableRow>
          </TableHeader>
          <TableBody>
            {listQuery.isPending && (
              <TableRow>
                <TableCell colSpan={listColumns.length + 1} className="text-center text-muted-foreground">
                  Loading…
                </TableCell>
              </TableRow>
            )}
            {listQuery.data?.results.length === 0 && (
              <TableRow>
                <TableCell colSpan={listColumns.length + 1} className="text-center text-muted-foreground">
                  No records yet.
                </TableCell>
              </TableRow>
            )}
            {listQuery.data?.results.map((row) => (
              <TableRow key={row.public_id as string}>
                {listColumns.map((f) => (
                  <TableCell key={f.name}>
                    {f.relation
                      ? (relationLabels[f.name]?.get(row[f.name] as string) ?? formatCell(row[f.name]))
                      : formatCell(row[f.name])}
                  </TableCell>
                ))}
                <TableCell className="flex justify-end gap-1">
                  {config.getDetailPath && (
                    <Button variant="ghost" size="icon" asChild>
                      <Link to={config.getDetailPath(row)}>
                        <Eye className="size-4" />
                      </Link>
                    </Button>
                  )}
                  <Button variant="ghost" size="icon" onClick={() => openEdit(row)}>
                    <Pencil className="size-4" />
                  </Button>
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={() => {
                      if (confirm(`Delete this ${config.label.toLowerCase()} record?`)) {
                        deleteMutation.mutate(row)
                      }
                    }}
                  >
                    <Trash2 className="size-4 text-destructive" />
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </Card>

      <Dialog open={dialogRow !== undefined} onOpenChange={(open) => !open && setDialogRow(undefined)}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>{dialogRow ? `Edit ${config.label}` : `New ${config.label}`}</DialogTitle>
          </DialogHeader>
          <ResourceForm
            fields={config.fields}
            values={formValues}
            onChange={(name, value) => setFormValues((prev) => ({ ...prev, [name]: value }))}
          />
          {formError && <p className="text-sm text-destructive">{formError}</p>}
          <DialogFooter>
            <Button variant="outline" onClick={() => setDialogRow(undefined)}>
              Cancel
            </Button>
            <Button onClick={() => saveMutation.mutate(formValues)} disabled={saveMutation.isPending}>
              {saveMutation.isPending ? "Saving…" : "Save"}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
}

/**
 * Resolves each relation column's public_id values to a human-readable
 * label, so list tables show "Ama Mensah" instead of a raw UUID. Shares
 * the same query cache key as RelationSelect, so opening a create/edit
 * dialog on the same page doesn't refetch.
 */
function useRelationLabelMaps(columns: FieldConfig[]): Record<string, Map<string, string> | undefined> {
  const relationColumns = columns.filter((f) => f.relation)
  const results = useQueries({
    queries: relationColumns.map((f) => ({
      queryKey: ["relation-options", f.relation!.endpoint],
      queryFn: () =>
        apiClient
          .get<Paginated<Record<string, unknown>>>(f.relation!.endpoint, { params: { page_size: 200 } })
          .then((r) => r.data.results),
    })),
  })

  return React.useMemo(() => {
    const maps: Record<string, Map<string, string> | undefined> = {}
    relationColumns.forEach((f, i) => {
      const data = results[i]?.data
      if (!data) return
      maps[f.name] = new Map(data.map((item) => [item.public_id as string, f.relation!.labelFn(item)]))
    })
    return maps
  }, [results, relationColumns.map((f) => f.name).join(",")]) // eslint-disable-line -- relationColumns re-derives each render; name-joined string keeps the dep stable
}

function cleanPayload(values: FormValues, fields: import("@/lib/resource-config").FieldConfig[]): Record<string, unknown> {
  const fieldByName = new Map(fields.map((f) => [f.name, f]))
  const out: Record<string, unknown> = {}
  for (const [key, value] of Object.entries(values)) {
    const field = fieldByName.get(key)
    if (field?.readOnly) continue
    if (field?.type === "tags") {
      out[key] = String(value)
        .split(",")
        .map((s) => s.trim())
        .filter(Boolean)
      continue
    }
    if (value === "") continue // omit empty optional fields rather than sending ""
    out[key] = value
  }
  return out
}

function formatCell(value: unknown): string {
  if (value === null || value === undefined || value === "") return "—"
  if (typeof value === "boolean") return value ? "Yes" : "No"
  if (Array.isArray(value)) return value.length ? value.join(", ") : "—"
  return String(value)
}

function extractError(err: unknown): string {
  if (isAxiosError(err)) {
    const data = err.response?.data as { error?: { message?: unknown } } | undefined
    const message = data?.error?.message
    if (typeof message === "string") return message
    if (message && typeof message === "object") return Object.values(message).flat().join(" ")
  }
  return "Something went wrong. Please try again."
}
