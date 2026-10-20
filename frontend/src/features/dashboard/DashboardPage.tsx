import { useQuery } from "@tanstack/react-query"
import { Users, CalendarClock, BedDouble, Receipt } from "lucide-react"

import { apiClient } from "@/lib/api-client"
import { useAuth } from "@/features/auth/AuthContext"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import type { Paginated } from "@/types/api"

const cards = [
  { label: "Patients", endpoint: "/patients/", icon: Users, to: "/patients" },
  { label: "Appointments", endpoint: "/appointments/", icon: CalendarClock, to: "/appointments" },
  { label: "Beds", endpoint: "/wards/beds/", icon: BedDouble, to: "/wards" },
  { label: "Invoices", endpoint: "/billing/invoices/", icon: Receipt, to: "/billing" },
]

export function DashboardPage() {
  const { user } = useAuth()

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-xl font-semibold">Welcome{user ? `, ${user.first_name}` : ""}</h1>
        <p className="text-sm text-muted-foreground">Here's a quick overview of the system.</p>
      </div>
      <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
        {cards.map((c) => (
          <StatCard key={c.label} {...c} />
        ))}
      </div>
    </div>
  )
}

function StatCard({
  label,
  endpoint,
  icon: Icon,
}: {
  label: string
  endpoint: string
  icon: typeof Users
  to: string
}) {
  const { data, isPending } = useQuery({
    queryKey: ["dashboard-count", endpoint],
    queryFn: () => apiClient.get<Paginated<unknown>>(endpoint, { params: { page_size: 1 } }).then((r) => r.data.count),
  })

  return (
    <Card>
      <CardHeader className="flex-row items-center justify-between gap-2 space-y-0 pb-2">
        <CardTitle className="text-sm font-medium text-muted-foreground">{label}</CardTitle>
        <Icon className="size-4 text-muted-foreground" />
      </CardHeader>
      <CardContent>
        <p className="text-2xl font-semibold">{isPending ? "…" : (data ?? "—")}</p>
      </CardContent>
    </Card>
  )
}
