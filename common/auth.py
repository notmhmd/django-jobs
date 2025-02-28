import time

import requests
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.core.cache import cache


class KeycloakAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get("Authorization")
        if not token:
            return None
        token = token.replace("Bearer ", "")

        cached_user_info = cache.get(f"keycloak_token_{token}")
        if cached_user_info:
            return cached_user_info, token

        url = f"{settings.KEYCLOAK_SERVER_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/userinfo"
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            raise AuthenticationFailed("Invalid token")

        user_info = response.json()
        exp = user_info.get("exp")
        if exp:
            ttl = max(exp - int(time.time()), 0)  # Ensure non-negative TTL
        else:
            ttl = 300  # Default cache timeout if expiration is missing
        cache.set(f"keycloak_token_{token}", user_info, timeout=ttl)
        return user_info, token


class IsAdminPermission(BaseAuthentication):
    def has_permission(self, request, view):
        user_roles = request.user.get("resource_access", {}).get("realm-management", {}).get("roles", [])
        return "view-users" in user_roles