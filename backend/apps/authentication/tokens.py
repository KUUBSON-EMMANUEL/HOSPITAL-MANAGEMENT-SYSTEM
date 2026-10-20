from datetime import timedelta

from rest_framework_simplejwt.tokens import Token


class MFAChallengeToken(Token):
    """Short-lived token issued after password verification when MFA is
    enabled, exchanged for real access/refresh tokens via
    POST /api/v1/auth/mfa/verify/. Distinct token_type keeps it from being
    usable as a normal access token even if leaked."""

    token_type = "mfa_challenge"
    lifetime = timedelta(minutes=5)
