from rest_framework.views import APIView
from authentications.auth import CustomAuthentication

class AuthAPIView(APIView):
    """
    assigning CustomAuthentication class to authentication_classes
    """
    authentication_classes = [CustomAuthentication, ]