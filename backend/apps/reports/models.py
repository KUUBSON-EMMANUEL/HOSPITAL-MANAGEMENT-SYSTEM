from django.conf import settings
from django.db import models

from apps.core.models import BaseModel, BranchScopedModel


class SavedReport(BaseModel, BranchScopedModel):
    name = models.CharField(max_length=200)
    report_type = models.CharField(max_length=100)
    parameters = models.JSONField(default=dict, blank=True)
    generated_at = models.DateTimeField(null=True, blank=True)
    generated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True, related_name="saved_reports"
    )
    output_file = models.FileField(upload_to="reports/", blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.name
