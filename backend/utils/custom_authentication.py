import datetime

import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from backend.settings import ALGORITHM, TOKEN_SECRET_KEY


class CustomJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        token = auth_header.split(" ", 1)[1]

        try:
            payload = jwt.decode(token, key=TOKEN_SECRET_KEY, algorithms=ALGORITHM)
            if (
                payload["exp"]
                < datetime.datetime.now(datetime.timezone.utc).timestamp()
            ):
                raise AuthenticationFailed("Token has expired")

            user = {
                "user_id": payload["user_id"],
                "group_id": payload["group_id"],
                "username": payload["username"],
                "role": payload["role"],
            }
            return (user, None)
        except jwt.DecodeError:
            raise AuthenticationFailed("Invalid token")
