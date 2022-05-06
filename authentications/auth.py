import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from credentials import SECRET_KEY, ALGO


class CustomAuthentication(BaseAuthentication):
    def authenticate(self, request):

        if 'Authorization' in request.headers:
            # token = request.headers["Authorization"]
            token = str(request.META['HTTP_AUTHORIZATION'][7:])
            try:
                user_data = {}
                payload = jwt.decode(token, SECRET_KEY, ALGO)
                print(payload)
                user_data["user_id"] = payload["id"]
                user_data["mobile"] = payload["mobile"]
                user_data["full_name"] = payload["full_name"]
            except jwt.DecodeError or jwt.InvalidTokenError:
                raise exceptions.AuthenticationFailed('Invalid authorization token')
        else:
            raise exceptions.AuthenticationFailed('Invalid authorization token')

        return user_data, None