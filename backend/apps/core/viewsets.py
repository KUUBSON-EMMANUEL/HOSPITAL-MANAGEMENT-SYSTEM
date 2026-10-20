from rest_framework import viewsets


class BaseModelViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet that populates AuditableModel's created_by/updated_by from
    the authenticated request user, fulfilling the contract described in
    apps.core.models.AuditableModel's docstring.

    Looks records up by public_id rather than DRF's default internal
    integer pk, matching UUIDPublicIDModel's whole point: external
    references (URLs, API responses) must never expose sequential
    database IDs. Every serializer already returns public_id as the
    canonical identifier (see PublicIdRelatedField) -- retrieve/update/
    delete need to accept that same value back in the URL.
    """

    lookup_field = "public_id"

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
