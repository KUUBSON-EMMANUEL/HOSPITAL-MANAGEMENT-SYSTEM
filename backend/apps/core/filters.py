import django_filters
from django.db import models


def build_filterset(model, field_names):
    """
    Builds a FilterSet for `model` covering `field_names`. ForeignKey fields
    filter against the related object's public_id rather than django-filter's
    default (the internal integer pk) -- every serializer represents
    relations via public_id (see PublicIdRelatedField), so a client can only
    ever supply a public_id as the filter value; matching on it directly
    keeps filtering consistent with what list/detail responses show.
    Non-FK fields (status, sex, ...) fall through to django-filter's normal
    exact-match behavior via Meta.fields.
    """
    attrs = {}
    plain_fields = []
    for name in field_names:
        field = model._meta.get_field(name)
        if isinstance(field, models.ForeignKey):
            attrs[name] = django_filters.CharFilter(field_name=f"{name}__public_id")
        else:
            plain_fields.append(name)

    attrs["Meta"] = type("Meta", (), {"model": model, "fields": plain_fields})
    return type(f"{model.__name__}FilterSet", (django_filters.FilterSet,), attrs)
