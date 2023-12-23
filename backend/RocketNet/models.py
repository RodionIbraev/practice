import uuid

from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.http import HttpResponseServerError
from django_softdelete.models import SoftDeleteModel

from .utils import add_change_balance_method, OperationType

STATE_CHOICES = (
    ("new", "Новый"),
    ("connected", "Подключен"),
    ("canceled", "Отменен"),
)


class User(AbstractUser, SoftDeleteModel):
    phone_number = models.CharField(max_length=128, unique=True, verbose_name="Номер телефона")
    password = models.CharField(max_length=128, verbose_name="Пароль")
    username = None

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Пользователи"
        verbose_name_plural = "Пользователи"
        ordering = ("first_name",)


class Account(models.Model):
    user = models.OneToOneField(User, verbose_name="Пользователь", editable=False, unique=True, db_index=True, on_delete=models.CASCADE)
    balance = models.DecimalField(verbose_name="Баланс", max_digits=10, decimal_places=2)

    @classmethod
    def deposit(cls, pk, amount):
        return add_change_balance_method(
            django_model=cls,
            django_field="balance",
            pk=pk,
            amount=amount,
            operation_type=OperationType.DEPOSIT,
        )

    def __str__(self) -> str:
        return f"Баланс пользователя: {self.user}"
    
    class Meta:
        verbose_name = "Баланс"
        verbose_name_plural = "Баланс"
        ordering = ["-user"]


class BalanceChange(models.Model):
    class OperationType(models.TextChoices):
        DEPOSIT = ("DT", "DEPOSIT")

    account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name="balance_changes",
    )

    amount = models.DecimalField(verbose_name="Сумма", max_digits=10, decimal_places=2,
        editable=False,
    )
    payment_uuid = models.UUIDField(verbose_name="Платеж", db_index=True, null=True)
    created_date = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        db_index=True,
    )
    is_accepted = models.BooleanField(default=False)

    operation_type = models.CharField(max_length=20, choices=OperationType.choices)

    def __str__(self) -> str:
        return (
            f"Баланс пользователя:  {self.account} "
            f"Время создания: {self.created_date}"
            f"Количество: {self.amount}"
        )

    class Meta:
        verbose_name = "Изменение баланса"
        verbose_name_plural = "Изменение баланса"
        ordering = ["-created_date"]


class MobileTariffPlan(SoftDeleteModel):
    name = models.CharField(max_length=128, verbose_name="Название")
    minutes = models.CharField(max_length=128, verbose_name="Минуты")
    sms = models.CharField(max_length=128, verbose_name="Сообщения")
    mobile_internet = models.CharField(max_length=128, verbose_name="Мобильный интернет")
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Стоимость")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Мобильные тарифные планы"
        verbose_name_plural = "Мобильные тарифные планы"
        ordering = ("-price",)


class HomeTariffPlan(SoftDeleteModel):
    name = models.CharField(max_length=128, verbose_name="Название")
    tv_channels = models.CharField(max_length=128, verbose_name="ТВ каналы")
    home_internet = models.CharField(max_length=128, verbose_name="Домашний интернет")
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Стоимость")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Домашние тарифные планы"
        verbose_name_plural = "Домашние тарифные планы"
        ordering = ("-price",)


class ComboTariffPlan(SoftDeleteModel):
    name = models.CharField(max_length=128, verbose_name="Название")
    tv_channels = models.CharField(max_length=128, verbose_name="ТВ каналы")
    home_internet = models.CharField(max_length=128, verbose_name="Домашний интернет")
    minutes = models.CharField(max_length=128, verbose_name="Минуты")
    sms = models.CharField(max_length=128, verbose_name="Сообщения")
    mobile_internet = models.CharField(max_length=128, verbose_name="Мобильный интернет")
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Стоимость")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Комбо-тарифные планы"
        verbose_name_plural = "Комбо-тарифные планы"
        ordering = ("-price",)


class Agreement(SoftDeleteModel):
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    mobile_tariff_plan = models.ForeignKey(MobileTariffPlan, verbose_name="Мобильный тариф",
                                           on_delete=models.DO_NOTHING, null=True, blank=True)
    home_tariff_plan = models.ForeignKey(HomeTariffPlan, verbose_name="Домашний тариф",
                                         on_delete=models.DO_NOTHING, null=True, blank=True)
    combo_tariff_plan = models.ForeignKey(ComboTariffPlan, verbose_name="Комбо-тариф",
                                          on_delete=models.DO_NOTHING, null=True, blank=True)
    state = models.CharField(verbose_name="Статус", choices=STATE_CHOICES, max_length=15)
    created_at = models.DateTimeField(auto_now=True, verbose_name="Дата заключения договора")

    def __str__(self):
        return f"{self.state} договор с {self.user}"

    class Meta:
        verbose_name = "Договоры"
        verbose_name_plural = "Договоры"
        ordering = ("user",)
