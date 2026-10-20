import type { LucideIcon } from "lucide-react"
import {
  LayoutDashboard,
  Users,
  CalendarClock,
  Stethoscope,
  ClipboardList,
  Clipboard,
  BedDouble,
  Receipt,
  Pill,
  FlaskConical,
  ScanLine,
  ShieldCheck,
  Boxes,
  UserCog,
  Siren,
  Scissors,
  Baby,
  Video,
  MessageSquare,
  Bell,
  FileBarChart,
  HeartPulse,
  History,
} from "lucide-react"

export interface NavItem {
  label: string
  to: string
  icon: LucideIcon
}

export interface NavGroup {
  label: string
  items: NavItem[]
}

export const navGroups: NavGroup[] = [
  {
    label: "Overview",
    items: [{ label: "Dashboard", to: "/", icon: LayoutDashboard }],
  },
  {
    label: "Clinical",
    items: [
      { label: "Patients", to: "/patients", icon: Users },
      { label: "Appointments", to: "/appointments", icon: CalendarClock },
      { label: "Encounters", to: "/ehr/encounters", icon: Stethoscope },
      { label: "Vital Signs", to: "/ehr/vitals", icon: HeartPulse },
      { label: "Consultations", to: "/consultations", icon: Clipboard },
      { label: "Nursing Notes", to: "/nursing", icon: ClipboardList },
    ],
  },
  {
    label: "Inpatient & Billing",
    items: [
      { label: "Wards & Beds", to: "/wards", icon: BedDouble },
      { label: "Billing", to: "/billing", icon: Receipt },
    ],
  },
  {
    label: "Diagnostics & Pharmacy",
    items: [
      { label: "Pharmacy", to: "/pharmacy", icon: Pill },
      { label: "Laboratory", to: "/laboratory", icon: FlaskConical },
      { label: "Radiology", to: "/radiology", icon: ScanLine },
    ],
  },
  {
    label: "Administration",
    items: [
      { label: "Insurance", to: "/insurance", icon: ShieldCheck },
      { label: "Inventory", to: "/inventory", icon: Boxes },
      { label: "Staff", to: "/staff", icon: UserCog },
      { label: "Branches", to: "/branches", icon: Boxes },
    ],
  },
  {
    label: "Specialized Care",
    items: [
      { label: "Emergency", to: "/emergency", icon: Siren },
      { label: "Theatre", to: "/theatre", icon: Scissors },
      { label: "Maternity", to: "/maternity", icon: Baby },
      { label: "Telemedicine", to: "/telemedicine", icon: Video },
    ],
  },
  {
    label: "Comms & Reports",
    items: [
      { label: "Messaging", to: "/messaging", icon: MessageSquare },
      { label: "Notifications", to: "/notifications", icon: Bell },
      { label: "Reports", to: "/reports", icon: FileBarChart },
      { label: "Audit Log", to: "/audit", icon: History },
    ],
  },
]
