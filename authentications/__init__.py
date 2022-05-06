from rest_framework.views import APIView
from authentications.auth import CustomAuthentication

class AuthAPIView(APIView):
    authentication_classes = [CustomAuthentication, ]