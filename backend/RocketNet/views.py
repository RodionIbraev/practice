import datetime
import jwt
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import UserSerializer

from functools import wraps


def auth_required(view_func):
    @wraps(view_func)
    def wrapper(self, request, *args, **kwargs):
        token = request.COOKIES.get('jwt_token')
        if not token:
            raise AuthenticationFailed('Не авторизован!')
        try:
            jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Не авторизован!')

        return view_func(self, request, *args, **kwargs)

    return wrapper


class RegisterView(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
        phone_number = request.data['phone_number']
        password = request.data['password']

        user = User.objects.filter(phone_number=phone_number).first()
        if user is None:
            raise AuthenticationFailed('Пользователя не существует!')

        if not user.check_password(password):
            raise AuthenticationFailed('Введён некорректный пароль!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()
        response.set_cookie(key='jwt_token', value=token, httponly=True)
        response.data = {
            'jwt_token': token
        }

        return response


class LogoutView(APIView):
    @auth_required
    def get(self, request):
        response = Response()
        response.delete_cookie('jwt_token')
        response.data = {
            'message': 'success logout!'
        }

        return response
