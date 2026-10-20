import uuid

from django.conf import settings
from django.db import models


class TimeStampedModel(models.Model):
    """Adds creation/update timestamps to any model."""

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDPublicIDModel(models.Model):
    """
    Adds a non-sequential public identifier alongside the internal BigAutoField
    primary key, so external references (QR codes, URLs, API responses) never
    leak sequential database IDs.
    """

    public_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)

    class Meta:
        abstract = True


class SoftDeleteQuerySet(models.QuerySet):
    def alive(self):
        return self.filter(deleted_at__isnull=True)

    def dead(self):
        return self.filter(deleted_at__isnull=False)

    def delete(self):
        from django.utils import timezone

        return self.update(deleted_at=timezone.now())

    def hard_delete(self):
        return super().delete()


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).alive()


class AllObjectsManager(models.Manager):
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db)


class SoftDeleteModel(models.Model):
    """
    Clinical and financial records are never hard-deleted for audit/compliance
    reasons; deletion marks a timestamp and the record is excluded from the
    default manager but remains queryable via `all_objects`.
    """

    deleted_at = models.DateTimeField(null=True, blank=True, db_index=True)

    objects = SoftDeleteManager()
    all_objects = AllObjectsManager()

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False, hard=False):
        if hard:
            return super().delete(using=using, keep_parents=keep_parents)
        from django.utils import timezone

        self.deleted_at = timezone.now()
        self.save(update_fields=["deleted_at"])
        return None

    def restore(self):
        self.deleted_at = None
        self.save(update_fields=["deleted_at"])


class AuditableModel(models.Model):
    """
    Tracks which authenticated staff member created/last modified a record.
    Populated automatically from the current request via CurrentRequestMiddleware
    in views/serializers that call `apps.core.middleware.get_current_user()`.
    """

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_created",
        on_delete=models.SET_NULL,
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_updated",
        on_delete=models.SET_NULL,
    )

    class Meta:
        abstract = True


class BranchScopedModel(models.Model):
    """
    Every clinical/operational record belongs to exactly one hospital branch,
    enabling multi-branch hospital support and per-branch data isolation.
    """

    branch = models.ForeignKey(
        "branches.Branch",
        related_name="%(app_label)s_%(class)s_set",
        on_delete=models.PROTECT,
    )

    class Meta:
        abstract = True


class BaseModel(TimeStampedModel, UUIDPublicIDModel, AuditableModel, SoftDeleteModel):
    """Standard base for most domain models across the system."""

    class Meta:
        abstract = True
