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
from .views import (RegisterView, LoginView, LogoutView, AccountDetailsView, TariffAndEquipmentPlansDetailsView,
                    CreatePaymentView,AcceptPaymentView, AgreementEquipmentRegistrationView,
                    AgreementEquipmentDeleteView, AgreementTariffRegistrationView, AgreementTariffDeleteView)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("personal-area/", AccountDetailsView.as_view(), name="personal-area"),
    path("", TariffAndEquipmentPlansDetailsView.as_view(), name="home-page"),
    path("create-payment/", CreatePaymentView.as_view(), name="create-payment"),
    path("agreement-tariff-registration/<str:tariff_type>/<str:tariff_id>", AgreementTariffRegistrationView.as_view(),
         name="agreement-tariff-registration"),
    path("agreement-equipment-registration/<str:equipment_id>",
         AgreementEquipmentRegistrationView.as_view(),
         name="agreement-tariff-registration"),
    path("agreement-tariff-delete/<str:tariff_type>/<str:tariff_id>", AgreementTariffDeleteView.as_view(),
         name="agreement-tariff-delete"),
    path("agreement-equipment-delete/<str:equipment_id>", AgreementEquipmentDeleteView.as_view(),
         name="agreement-equipment-delete"),
    path("accept-payment/<str:balance_change_id>/", AcceptPaymentView.as_view(), name="accept-payment"),
]
