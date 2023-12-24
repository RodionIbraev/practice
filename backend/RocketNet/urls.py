"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path("", views.home, name="home")
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path("", Home.as_view(), name="home")
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path("blog/", include("blog.urls"))
"""
from django.urls import path
from .views import RegisterView, LoginView, LogoutView, AccountDetailsView, TariffPlansDetailsView, CreatePaymentView, \
    AcceptPaymentView, AgreementRegistrationView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("personal-area/", AccountDetailsView.as_view(), name="personal-area"),
    path("", TariffPlansDetailsView.as_view(), name="home-page"),
    path("create-payment/", CreatePaymentView.as_view(), name="create-payment"),
    path("agreement-registration/<str:tariff_id_and_type>", AgreementRegistrationView.as_view(), name="agreement-registration"),
    path("accept-payment/<str:balance_change_id>/", AcceptPaymentView.as_view(), name="create-payment"),
]
