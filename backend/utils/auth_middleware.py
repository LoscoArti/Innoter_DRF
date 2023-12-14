import datetime

from django.http import JsonResponse
from jwt import decode, exceptions

from backend.settings import ALGORITHM, TOKEN_SECRET_KEY


class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path in ["/favicon.ico", "/admin/"]:
            # Allow access to the admin panel without a token
            return self.get_response(request)

        token = self.get_token_from_request(request)
        if not token:
            return self.build_unauthorized_response()

        try:
            payload = decode(token, key=TOKEN_SECRET_KEY, algorithms=ALGORITHM)
            if (
                payload["exp"]
                < datetime.datetime.now(datetime.timezone.utc).timestamp()
            ):
                return self.build_unauthorized_response()
        except exceptions.DecodeError:
            return self.build_unauthorized_response()

        user_info = {
            "user_id": payload["user_id"],
            "group_id": payload["group_id"],
            "username": payload["username"],
            "role": payload["role"],
        }

        request.user = user_info

        response = self.get_response(request)

        return response

    def get_token_from_request(self, request):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        _, token = auth_header.split(" ", 1)
        return token

    def build_unauthorized_response(self):
        return JsonResponse({"error": "Unauthorized"}, status=401)
