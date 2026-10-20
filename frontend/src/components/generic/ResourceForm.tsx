import type { FieldConfig } from "@/lib/resource-config"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { RelationSelect } from "./RelationSelect"

export type FormValues = Record<string, string | boolean>

export function ResourceForm({
  fields,
  values,
  onChange,
}: {
  fields: FieldConfig[]
  values: FormValues
  onChange: (name: string, value: string | boolean) => void
}) {
  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
      {fields.map((field) => (
        <div
          key={field.name}
          className={field.type === "textarea" ? "flex flex-col gap-1.5 sm:col-span-2" : "flex flex-col gap-1.5"}
        >
          <Label htmlFor={field.name}>
            {field.label}
            {field.required && <span className="text-destructive"> *</span>}
          </Label>
          <FieldInput field={field} value={values[field.name]} onChange={(v) => onChange(field.name, v)} />
        </div>
      ))}
    </div>
  )
}

function FieldInput({
  field,
  value,
  onChange,
}: {
  field: FieldConfig
  value: string | boolean | undefined
  onChange: (value: string | boolean) => void
}) {
  if (field.readOnly) {
    return (
      <Input id={field.name} value={(value as string) ?? "(auto-generated)"} disabled />
    )
  }

  if (field.relation) {
    return (
      <RelationSelect
        relation={field.relation}
        value={(value as string) ?? ""}
        onChange={onChange}
        required={field.required}
      />
    )
  }

  if (field.type === "select" && field.options) {
    return (
      <Select value={(value as string) || undefined} onValueChange={onChange}>
        <SelectTrigger>
          <SelectValue placeholder="Select…" />
        </SelectTrigger>
        <SelectContent>
          {field.options.map((opt) => (
            <SelectItem key={opt.value} value={opt.value}>
              {opt.label}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    )
  }

  if (field.type === "tags") {
    return (
      <Input
        id={field.name}
        value={(value as string) ?? ""}
        onChange={(e) => onChange(e.target.value)}
        placeholder="Comma-separated, e.g. penicillin, peanuts"
      />
    )
  }

  if (field.type === "textarea") {
    return (
      <Textarea
        id={field.name}
        value={(value as string) ?? ""}
        onChange={(e) => onChange(e.target.value)}
        required={field.required}
      />
    )
  }

  if (field.type === "checkbox") {
    return (
      <input
        id={field.name}
        type="checkbox"
        className="size-4"
        checked={Boolean(value)}
        onChange={(e) => onChange(e.target.checked)}
      />
    )
  }

  return (
    <Input
      id={field.name}
      type={field.type}
      value={(value as string) ?? ""}
      onChange={(e) => onChange(e.target.value)}
      required={field.required}
    />
  )
}
