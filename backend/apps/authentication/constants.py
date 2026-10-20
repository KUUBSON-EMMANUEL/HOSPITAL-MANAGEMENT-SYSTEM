from django.db import models


class RoleCode(models.TextChoices):
    """
    Canonical set of staff roles across the hospital. Fine-grained access
    beyond "which role" (e.g. which modules a role may edit vs. view) is
    expressed through Role -> Permission assignments (see models.Role),
    so this list defines *who* a user is, not what they may do.
    """

    SUPER_ADMIN = "SUPER_ADMIN", "Super Administrator"
    BRANCH_ADMIN = "BRANCH_ADMIN", "Branch Administrator"
    DOCTOR = "DOCTOR", "Doctor / Physician"
    NURSE = "NURSE", "Nurse"
    RECEPTIONIST = "RECEPTIONIST", "Front Desk / Receptionist"
    LAB_TECHNICIAN = "LAB_TECHNICIAN", "Laboratory Technician"
    RADIOLOGIST = "RADIOLOGIST", "Radiologist / Imaging Technician"
    PHARMACIST = "PHARMACIST", "Pharmacist"
    INVENTORY_MANAGER = "INVENTORY_MANAGER", "Inventory / Supply Chain Manager"
    BILLING_CLERK = "BILLING_CLERK", "Billing Clerk"
    INSURANCE_OFFICER = "INSURANCE_OFFICER", "Insurance Officer"
    WARD_MANAGER = "WARD_MANAGER", "Ward Manager"
    THEATRE_STAFF = "THEATRE_STAFF", "Operating Theatre Staff"
    MATERNITY_STAFF = "MATERNITY_STAFF", "Maternity Ward Staff"
    HR_MANAGER = "HR_MANAGER", "Human Resources Manager"
    IT_ADMIN = "IT_ADMIN", "IT Administrator"
    COMPLIANCE_OFFICER = "COMPLIANCE_OFFICER", "Compliance / Audit Officer"


class ModuleCode(models.TextChoices):
    """One entry per HMS module; used to scope granular Permission rows."""

    AUTHENTICATION = "authentication", "Authentication & User Management"
    PATIENTS = "patients", "Patient Registration"
    EHR = "ehr", "Electronic Health Records"
    CONSULTATIONS = "consultations", "Consultation Management"
    NURSING = "nursing", "Nursing Management"
    LABORATORY = "laboratory", "Laboratory Information System"
    RADIOLOGY = "radiology", "Radiology Information System"
    PHARMACY = "pharmacy", "Pharmacy Management"
    INVENTORY = "inventory", "Inventory Management"
    BILLING = "billing", "Billing and Payments"
    INSURANCE = "insurance", "Insurance Management"
    APPOINTMENTS = "appointments", "Appointment Scheduling"
    WARDS = "wards", "Inpatient Ward Management"
    EMERGENCY = "emergency", "Emergency Unit Management"
    THEATRE = "theatre", "Operating Theatre Management"
    MATERNITY = "maternity", "Maternity Management"
    TELEMEDICINE = "telemedicine", "Telemedicine"
    STAFF = "staff", "Staff Management"
    REPORTS = "reports", "Reporting and Analytics"
    AUDIT = "audit", "Audit and Compliance"
    NOTIFICATIONS = "notifications", "Notification System"
    MESSAGING = "messaging", "Internal Messaging"
    BRANCHES = "branches", "Multi-Branch Administration"


class PermissionAction(models.TextChoices):
    VIEW = "view", "View"
    CREATE = "create", "Create"
    EDIT = "edit", "Edit"
    DELETE = "delete", "Delete"
    APPROVE = "approve", "Approve"
    EXPORT = "export", "Export"
