import datetime
import os

import jwt
from django.contrib.auth.password_validation import validate_password
from django.forms import model_to_dict
from django.shortcuts import redirect
from dotenv import load_dotenv
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_201_CREATED
from rest_framework.views import APIView

from .models import User, Agreement, MobileTariffPlan, HomeTariffPlan, ComboTariffPlan, Account
from .serializers import UserSerializer, CreatePaymentSerializer

from functools import wraps

from .services.create_payment import create_payment
from .services.payment_acceptance import payment_acceptance


load_dotenv()


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
    user = User.objects.get(id=payload["id"])
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

            Account.objects.create(
                user_id=serializer.data["id"],
                balance=0
            )

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


class TariffPlansDetailsView(APIView):
    """
    Просмотр тарифов
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "homePage.html"

    def get(self, request):
        token = request.COOKIES.get("jwt_token")
        if token:
            token = "token"
        mobile_tariff_plans = [mobile_tariff_plan for mobile_tariff_plan in MobileTariffPlan.objects.all().values()]
        home_tariff_plans = [home_tariff_plans for home_tariff_plans in HomeTariffPlan.objects.all().values()]
        combo_tariff_plans = [combo_tariff_plans for combo_tariff_plans in ComboTariffPlan.objects.all().values()]
        response = Response()
        response.data = {
            "mobile_tariff_plans": mobile_tariff_plans,
            "home_tariff_plans": home_tariff_plans,
            "combo_tariff_plans": combo_tariff_plans,
            "token": token
        }
        return response


class AccountDetailsView(APIView):
    """
    Личный кабинет пользователя
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "personalArea.html"

    @auth_required
    def get(self, request):
        user = User.objects.get(id=get_user(request).id)
        user_serializer = UserSerializer(user)
        user_account = Account.objects.get(user_id=get_user(request).id)
        user_agreements = [agreement for agreement in Agreement.objects.filter(user=user.id).values()]

        user_mobile_tariffs = []
        user_home_tariffs = []
        user_combo_tariffs = []
        for agreement in user_agreements:
            mobile_tariff_id = agreement.get('mobile_tariff_plan_id')
            home_tariff_id = agreement.get('home_tariff_plan_id')
            combo_tariff_id = agreement.get('combo_tariff_plan_id')

            if mobile_tariff_id is not None:
                user_mobile_tariffs.append(MobileTariffPlan.objects.get(id=mobile_tariff_id))
            if home_tariff_id is not None:
                user_home_tariffs.append(HomeTariffPlan.objects.get(id=home_tariff_id))
            if combo_tariff_id is not None:
                user_combo_tariffs.append(ComboTariffPlan.objects.get(id=combo_tariff_id))

        response = Response()
        response.data = {
            "user": user_serializer.data,
            "user_agreements": user_agreements,
            "user_account": user_account,
            "user_mobile_tariffs": user_mobile_tariffs,
            "user_home_tariffs": user_home_tariffs,
            "user_combo_tariffs": user_combo_tariffs,
            "return_url": "https://" + os.getenv("NGROK_HOST") + "/accept-payment/"
        }
        return response


class AgreementRegistrationView(APIView):
    @auth_required
    def post(self, request, tariff_type, tariff_id):
        """
        Оформление договора пользователем
        """

        user = User.objects.get(id=get_user(request).id)
        if tariff_type == "mobile_tariff_plan":
            new_agreement = Agreement.objects.create(user=user, mobile_tariff_plan_id=tariff_id)
        elif tariff_type == "home_tariff_plan":
            new_agreement = Agreement.objects.create(user=user, home_tariff_plan_id=tariff_id)
        else:
            new_agreement = Agreement.objects.create(user=user, combo_tariff_plan_id=tariff_id)

        response = Response()
        response.data = {
            "new_agreement": model_to_dict(new_agreement),
            "created_at": new_agreement.created_at
        }
        return response


class CreatePaymentView(APIView):
    serializer_class = CreatePaymentSerializer

    @auth_required
    def post(self, request):
        try:
            serializer = CreatePaymentSerializer(data=request.data)
        except Exception as ex:
            return Response({"message": ex}, status=HTTP_500_INTERNAL_SERVER_ERROR)

        if serializer.is_valid(raise_exception=True):
            payment = create_payment(serializer.data)
            return Response(
                {
                    'payment': payment,
                    'confirmation_url': payment.confirmation.confirmation_url,
                 },
                status=HTTP_201_CREATED,
            )
        return Response({"message": serializer.errors}, status=HTTP_500_INTERNAL_SERVER_ERROR)


class AcceptPaymentView(APIView):
    @auth_required
    def get(self, request, balance_change_id):
        check_payment = payment_acceptance(balance_change_id)
        if check_payment["result"]:
            user_id = get_user(request).id
            user_account_id = Account.objects.get(user_id=user_id).id
            Account.deposit(pk=user_account_id, amount=check_payment["amount"])
        return redirect("personal-area")
