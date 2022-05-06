from rest_framework.authentication import BaseAuthentication


class CustomAuthentication(BaseAuthentication):
    def authenticate(self, request):

        if 'Authorization' in request.headers:
            token = request.headers["Authorization"]
            try:
                user_data = {}
                payload = jwt.decode(token, key)
                user_data["user_id"] = payload["user_id"]
                user_data["mobile"] = payload["mobile"]
                user_data["full_name"] = payload["full_name"]
            except jwt.ExpiredSignature or jwt.DecodeError or jwt.InvalidTokenError:
                raise exceptions.AuthenticationFailed('Invalid authorization token')
        else:
            raise exceptions.AuthenticationFailed('Invalid authorization token')

        return user_data, None