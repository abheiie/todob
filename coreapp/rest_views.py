from rest_framework.views import APIView
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from credentials import SECRET_KEY, ALGO
from controllers import get_user_by_mobile, create_user, get_user_by_mobile_and_password
from constants import LOGIN_TOKEN_EXPIRE_TIMEOUT


class Register(APIView):
    def post(self, request):
        requested_data = request.data
        full_name = requested_data.get("full_name")
        mobile = requested_data.get("mobile")
        password = requested_data.get("password")

        if not full_name or not mobile or not password:
            response = "Please fill in all of the fields."
            return Response(data=response, status=HTTP_400_BAD_REQUEST)

        existing_user = get_user_by_mobile(mobile)

        # check if user already exit with give mobile number
        if existing_user:
            response = "The email address is already being used."
            return Response(data=response, status=HTTP_400_BAD_REQUEST)

        # create a brand-new user
        user = create_user(full_name, mobile, password)
        return Response(data=user, status=HTTP_200_OK)


class Login(APIView):
    def post(self, request):
        requested_data = request.data
        mobile = requested_data.get("mobile")
        password = requested_data.get("password")
        user = get_user_by_mobile_and_password(mobile, password)

        if not user:
            response = "Your mobile and password combination does not match an account."
            return Response(data=response, status=HTTP_400_BAD_REQUEST)

        if user:
            payload = {
                "user": user
            }
            token = jwt.encode(payload, SECRET_KEY, ALGO, {"expires_in": LOGIN_TOKEN_EXPIRE_TIMEOUT})
            data = {
                "user": user,
                "token": token
            }
            return Response(data=data, status=HTTP_200_OK)



