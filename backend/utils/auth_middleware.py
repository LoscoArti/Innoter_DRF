import jwt
from django.conf import settings
from django.http import JsonResponse


class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/admin/"):
            # Skip authentication for Django admin
            return self.get_response(request)

        token = self.get_token_from_request(request)
        if not token:
            return self.build_unauthorized_response()

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.DecodeError:
            return self.build_unauthorized_response()

        # Attach the authenticated user to the request object
        request.user = payload["user"]

        response = self.get_response(request)

        return response

    def get_token_from_request(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None

        parts = auth_header.split()
        if parts[0].lower() != "bearer":
            return None

        if len(parts) == 1:
            return None

        if len(parts) > 2:
            return None

        return parts[1]

    def build_unauthorized_response(self):
        return JsonResponse({"error": "Unauthorized"}, status=401)
