from rest_framework import serializers


class PublicIdRelatedField(serializers.SlugRelatedField):
    """
    Relates via the target model's public_id (UUID) instead of its internal
    integer pk, so foreign-key fields in API requests/responses never leak
    sequential database IDs -- consistent with why UUIDPublicIDModel exists
    (see apps.core.models). Use for every FK field on every serializer:
        branch = PublicIdRelatedField(queryset=Branch.objects.all())
    """

    def __init__(self, **kwargs):
        kwargs.setdefault("slug_field", "public_id")
        super().__init__(**kwargs)
