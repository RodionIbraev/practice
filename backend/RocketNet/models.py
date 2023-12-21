from django.db import models
from django.contrib.auth.models import AbstractUser
from django_softdelete.models import SoftDeleteModel


class MobileTariffPlan(SoftDeleteModel):
    name = models.CharField(max_length=128, verbose_name="Название")

    def __str__(self):
        return f"{self.name}"


class HomeTariffPlan(SoftDeleteModel):
    name = models.CharField(max_length=128, verbose_name="Название")

    def __str__(self):
        return f"{self.name}"


class User(AbstractUser, SoftDeleteModel):
    phone_number = models.CharField(max_length=128, unique=True, verbose_name="Номер телефона")
    password = models.CharField(max_length=128, verbose_name="Пароль")
    username = None

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.name} {self.second_name}"

    class Meta:
        verbose_name = "Users"
        verbose_name_plural = "Пользователи"
        ordering = ("first_name",)


class Agreement(SoftDeleteModel):
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    mobile_tariff_plan = models.ForeignKey(MobileTariffPlan, verbose_name="Мобильный тариф",
                                           on_delete=models.CASCADE, null=True, blank=True)
    home_tariff_plan = models.ForeignKey(HomeTariffPlan, verbose_name="Мобильный тариф",
                                         on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True, verbose_name="Дата заключения договора")

    class Meta:
        verbose_name = "Agreements"
        verbose_name_plural = "Договоры"
        ordering = ("user",)
