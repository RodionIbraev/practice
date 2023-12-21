import datetime
import jwt
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, Agreement
from .serializers import UserSerializer

from functools import wraps


def auth_required(view_func):
    @wraps(view_func)
    def wrapper(self, request, *args, **kwargs):
        token = request.COOKIES.get("jwt_token")
        if not token:
            raise AuthenticationFailed("Не авторизован!")
        try:
            jwt.decode(token, "secret", algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Не авторизован!")

        return view_func(self, request, *args, **kwargs)

    return wrapper


def get_user(request):
    token = request.COOKIES.get("jwt_token")
    payload = jwt.decode(token, "secret", algorithms=["HS256"])
    user = User.objects.filter(id=payload["id"])
    return user


class RegisterView(APIView):
    """
    Регистрация пользователей
    """

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        # Проверка пароля на сложность
        try:
            validate_password(request.data["password"])
        except Exception as password_error:
            error_array = []
            for item in password_error:
                error_array.append(item)
            response = Response()
            response.data = {
                "Status": False,
                "Errors": {"password": error_array}
            }
            return response

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


class LoginView(APIView):
    """
    Аунтификация пользователей
    """

    def post(self, request):
        phone_number = request.data["phone_number"]
        password = request.data["password"]

        user = User.objects.filter(phone_number=phone_number).first()
        if user is None:
            raise AuthenticationFailed("Пользователя не существует!")

        if not user.check_password(password):
            raise AuthenticationFailed("Введён некорректный пароль!")

        payload = {
            "id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            "iat": datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, "secret", algorithm="HS256")

        response = Response()
        response.set_cookie(key="jwt_token", value=token, httponly=True)
        response.data = {
            "jwt_token": token
        }

        return response


class LogoutView(APIView):
    """
    Выход пользователей
    """

    @auth_required
    def get(self, request):
        response = Response()
        response.delete_cookie("jwt_token")
        response.data = {
            "message": "success logout!"
        }

        return response


class AccountDetailsView(APIView):
    """
    Личный кабинет пользователя
    """

    @auth_required
    def get(self, request):
        user = User.objects.get(id=get_user(request).id)
        user_serializer = UserSerializer(user)
        user_agreements = Agreement.objects.filter(user=user.id)
        user_agreements = [agreement for agreement in user_agreements.values()]
        response = Response()
        response.data = {
            "user": user_serializer.data,
            "user_agreements": user_agreements
        }
        return response
