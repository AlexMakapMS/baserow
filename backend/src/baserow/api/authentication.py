import jwt
from django.apps import apps
from django.utils.translation import gettext as _
from drf_spectacular.extensions import OpenApiAuthenticationExtension
from rest_framework import exceptions
from rest_framework_jwt.authentication import (
    JSONWebTokenAuthentication as JWTJSONWebTokenAuthentication,
)
from rest_framework_jwt.blacklist.exceptions import (
    MissingToken,
)
from rest_framework_jwt.compat import ExpiredSignature


class JSONWebTokenAuthentication(JWTJSONWebTokenAuthentication):
    def authenticate(self, request):
        """
        This method is basically a copy of
        rest_framework_jwt.authentication.BaseJSONWebTokenAuthentication.authenticate
        it adds a machine readable errors to the responses.

        Returns a two-tuple of `User` and token if a valid signature has been
        supplied using JWT-based authentication.  Otherwise returns `None`.
        """

        try:
            token = self.get_token_from_request(request)
            if token is None:
                return None
        except MissingToken:
            return None

        try:
            payload = self.jwt_decode_token(token)
        except ExpiredSignature:
            msg = _("Token has expired.")
            raise exceptions.AuthenticationFailed(
                {"detail": msg, "error": "ERROR_SIGNATURE_HAS_EXPIRED"}
            )
        except jwt.DecodeError:
            msg = _("Error decoding token.")
            raise exceptions.AuthenticationFailed(
                {"detail": msg, "error": "ERROR_DECODING_SIGNATURE"}
            )
        except jwt.InvalidTokenError:
            msg = _("Invalid token.")
            raise exceptions.AuthenticationFailed(msg)

        if apps.is_installed("rest_framework_jwt.blacklist"):
            from rest_framework_jwt.blacklist.models import BlacklistedToken

            if BlacklistedToken.is_blocked(token, payload):
                msg = _("Token is blacklisted.")
                raise exceptions.PermissionDenied(
                    {"detail": msg, "error": "ERROR_PERMISSION_DENIED"}
                )
        user = self.authenticate_credentials(payload)

        # @TODO this should actually somehow be moved to the ws app.
        user.web_socket_id = request.headers.get("WebSocketId")

        return user, token


class JSONWebTokenAuthenticationExtension(OpenApiAuthenticationExtension):
    target_class = "baserow.api.authentication.JSONWebTokenAuthentication"
    name = "JWT"
    match_subclasses = True
    priority = -1

    def get_security_definition(self, auto_schema):
        return {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT your_token",
        }
