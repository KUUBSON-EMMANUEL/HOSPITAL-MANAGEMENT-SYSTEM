import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class ComplexityValidator:
    """Requires an uppercase letter, a lowercase letter, a digit, and a
    symbol -- layered on top of the length/similarity/common-password/numeric
    validators already configured alongside it in AUTH_PASSWORD_VALIDATORS."""

    def validate(self, password, user=None):
        missing = []
        if not re.search(r"[A-Z]", password):
            missing.append(_("an uppercase letter"))
        if not re.search(r"[a-z]", password):
            missing.append(_("a lowercase letter"))
        if not re.search(r"\d", password):
            missing.append(_("a digit"))
        if not re.search(r"[^\w\s]", password):
            missing.append(_("a symbol"))
        if missing:
            raise ValidationError(
                _("Password must contain at least %(items)s.") % {"items": ", ".join(missing)},
                code="password_no_complexity",
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least one uppercase letter, one lowercase letter, "
            "one digit, and one symbol."
        )
