import jwt
from rest_framework.views import APIView
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND, \
    HTTP_401_UNAUTHORIZED, HTTP_204_NO_CONTENT
from rest_framework.response import Response
from credentials import SECRET_KEY, ALGO
from authentications import AuthAPIView
from .constants import collections, LOGIN_TOKEN_EXPIRE_TIMEOUT
from authentications import AuthAPIView
from .controllers import get_user_by_mobile, create_user, get_user_by_mobile_and_password, \
    get_all_todo, create_new_todo, update_todo, get_auth_user
from todob.settings import DB

todos_collection = DB[collections.get("todos")]


class Register(APIView):
    """
    Register a new user
    """
    def post(self, request):
        requested_data = request.data
        full_name = requested_data.get("full_name").strip() if requested_data.get("full_name") is not None else ""
        mobile = requested_data.get("mobile").strip() if requested_data.get("mobile") is not None else ""
        password = requested_data.get("password").strip() if requested_data.get("password") is not None else ""

        if not full_name or not mobile or not password:
            response = "Full Name, Mobile or password can't be blank."
            return Response(data=response, status=HTTP_400_BAD_REQUEST)

        if len(full_name) > 20:
            response = "Length of Full Name can't be more than 20 character"
            return Response(data=response, status=HTTP_400_BAD_REQUEST)

        if len(password) > 12:
            response = "Length of Password can't be more than 12 character"
            return Response(data=response, status=HTTP_400_BAD_REQUEST)

        if len(mobile) != 10:
            response = "Length of Mobile can be only of 10 digits"
            return Response(data=response, status=HTTP_400_BAD_REQUEST)
        
        if not mobile.isdigit():
            response = "Mobile number can contain digits only"
            return Response(data=response, status=HTTP_400_BAD_REQUEST)

        existing_user = get_user_by_mobile(mobile)

        # check if user already exit with give mobile number
        if existing_user:
            response = "The mobile number is already being used."
            return Response(data=response, status=HTTP_400_BAD_REQUEST)

        # create a brand-new user
        user = create_user(full_name, mobile, password)
        return Response(data=user, status=HTTP_201_CREATED)


class Login(APIView):
    """
    Login a user
    """
    def post(self, request):
        requested_data = request.data
        mobile = requested_data.get("mobile").strip() if requested_data.get("mobile") is not None else ""
        password = requested_data.get("password").strip() if requested_data.get("password") is not None else ""

        if not mobile or not password:
            response = "Mobile or password can't be blank."
            return Response(data=response, status=HTTP_400_BAD_REQUEST)

        user = get_user_by_mobile_and_password(mobile, password)
        if not user:
            response = "Your mobile and password combination does not match an account."
            return Response(data=response, status=HTTP_400_BAD_REQUEST)

        if user:
            payload = user
            token = jwt.encode(payload, SECRET_KEY, ALGO, {"expires_in": LOGIN_TOKEN_EXPIRE_TIMEOUT})
            data = {
                "user": user,
                "token": token
            }
            return Response(data=data, status=HTTP_200_OK)


class AuthUser(AuthAPIView):
    """
    get an authenticated user
    """
    def get(self, request):
        user_id = request.user.get("user_id")
        user = get_auth_user(user_id)
        return Response(data = user, status=HTTP_200_OK)


class TodoList(AuthAPIView):
    """
    List all todos, or create a new todo.
    """
    def get(self, request, format=None):
        user_id = request.user.get("user_id")
        todos = get_all_todo(user_id)
        return Response(data=todos, status=HTTP_200_OK)

    def post(self, request, format=None):
        requested_data = request.data
        user_id = request.user.get("user_id")
        body = requested_data.get("body").strip() if requested_data.get("body") is not None else ""
        if not body:
            response = "Length of todo body can't be blank"
            return Response(data=response, status=HTTP_400_BAD_REQUEST)
        if len(body) > 250:
            response = "Length of todo body can't be more than 250 character"
            return Response(data=response, status=HTTP_400_BAD_REQUEST)
        todo = create_new_todo(user_id, body)
        return Response(data=todo, status=HTTP_201_CREATED)


class TodoDetail(AuthAPIView):
    """
    Retrieve, update or delete a todo instance.
    """
    def get(self, request, id, format=None):
        user_id = request.user.get("user_id")
        todo = todos_collection.find_one({"id": id, "user_id": user_id}, {"_id": 0})
        if todo is not None:
            return Response(data=todo, status=HTTP_200_OK)
        else:
            response = "No TODO found"
            return Response(data=response, status=HTTP_404_NOT_FOUND)

    def put(self, request, id, format=None):
        user_id = request.user.get("user_id")
        todo = todos_collection.find_one({"id": id, "user_id": user_id}, {"_id": 0})
        requested_data = request.data
        body = requested_data.get("body").strip() if requested_data.get("body") is not None else ""
        if not body:
            response = "Length of todo body can't be blank"
            return Response(data=response, status=HTTP_400_BAD_REQUEST)
        if len(body) > 250:
            response = "Length of todo body can't be more than 250 character"
            return Response(data=response, status=HTTP_400_BAD_REQUEST)
        if not todo:
            response = "No TODO found to update"
            return Response(data=response, status=HTTP_404_NOT_FOUND)
        todo = update_todo(id, user_id, body)
        return Response(data=todo, status=HTTP_201_CREATED)

    def delete(self, request, id, format=None):
        user_id = request.user.get("user_id")
        todo = todos_collection.find_one({"id": id, "user_id": user_id}, {"_id": 0})
        if todo is not None:
            todos_collection.delete_one({"id": id, "user_id": user_id})
            response = "TODO deleted successfully"
            return Response(data=response, status=HTTP_204_NO_CONTENT)
        else:
            response = "No TODO found"
            return Response(data=response, status=HTTP_404_NOT_FOUND)








