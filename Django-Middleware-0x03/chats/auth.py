#!/usr/bin/env python3
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed


class CustomJWTAuthentication(JWTAuthentication):
    """
    Custom JWT authentication class.
    Extends SimpleJWT's JWTAuthentication to allow for custom checks.
    """

    def authenticate(self, request):
        """
        Override authenticate method if you want to add logging,
        IP checks, or user activity validation.
        """
        auth_result = super().authenticate(request)

        if auth_result is None:
            return None

        user, validated_token = auth_result

        # Example: prevent inactive users from authenticating
        if not user.is_active:
            raise AuthenticationFailed("User account is disabled.")

        return user, validated_token
