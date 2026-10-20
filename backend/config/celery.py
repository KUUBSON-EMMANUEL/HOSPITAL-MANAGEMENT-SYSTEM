import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")

app = Celery("hms")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "purge-expired-sessions": {
        "task": "apps.authentication.tasks.purge_expired_sessions",
        "schedule": crontab(hour=2, minute=0),
    },
    "appointment-reminders": {
        "task": "apps.appointments.tasks.send_appointment_reminders",
        "schedule": crontab(minute="*/15"),
    },
    "low-stock-alerts": {
        "task": "apps.inventory.tasks.check_low_stock_levels",
        "schedule": crontab(hour="*/4", minute=0),
    },
    "insurance-claim-followups": {
        "task": "apps.insurance.tasks.follow_up_pending_claims",
        "schedule": crontab(hour=6, minute=0),
    },
    "audit-log-archival": {
        "task": "apps.audit.tasks.archive_old_audit_logs",
        "schedule": crontab(hour=3, minute=0, day_of_week=0),
    },
}
