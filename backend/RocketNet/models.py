from django.db import models
from django.contrib.auth.models import AbstractUser
from django_softdelete.models import SoftDeleteModel

STATE_CHOICES = (
    ('new', 'Новый'),
    ('connected', 'Подключен'),
    ('canceled', 'Отменен'),
)


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


class MobileTariffPlan(SoftDeleteModel):
    name = models.CharField(max_length=128, verbose_name="Название")
    minutes = models.CharField(max_length=128, verbose_name="Минуты")
    sms = models.CharField(max_length=128, verbose_name="Сообщения")
    mobile_internet = models.CharField(max_length=128, verbose_name="Мобильный интернет")
    price = models.FloatField(verbose_name="Стоимость")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "MobileTariffPlans"
        verbose_name_plural = "Мобильные тарифные планы"
        ordering = ("-price",)


class HomeTariffPlan(SoftDeleteModel):
    name = models.CharField(max_length=128, verbose_name="Название")
    tv_channels = models.CharField(max_length=128, verbose_name="ТВ каналы")
    home_internet = models.CharField(max_length=128, verbose_name="Мобильный интернет")
    price = models.FloatField(verbose_name="Стоимость")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "HomeTariffPlans"
        verbose_name_plural = "Домашние тарифные планы"
        ordering = ("-price",)


class ComboTariffPlan(SoftDeleteModel):
    name = models.CharField(max_length=128, verbose_name="Название")
    mobile_tariff_plan = models.ForeignKey(MobileTariffPlan, verbose_name="Мобильный тариф",
                                           on_delete=models.CASCADE, null=True, blank=True)
    home_tariff_plan = models.ForeignKey(HomeTariffPlan, verbose_name="Мобильный тариф",
                                         on_delete=models.CASCADE, null=True, blank=True)
    price = models.FloatField(verbose_name="Стоимость")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "ComboTariffPlans"
        verbose_name_plural = "Комбо тарифные планы"
        ordering = ("-price",)


class Agreement(SoftDeleteModel):
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    mobile_tariff_plan = models.ForeignKey(MobileTariffPlan, verbose_name="Мобильный тариф",
                                           on_delete=models.DO_NOTHING, null=True, blank=True)
    home_tariff_plan = models.ForeignKey(HomeTariffPlan, verbose_name="Домашний тариф",
                                         on_delete=models.DO_NOTHING, null=True, blank=True)
    combo_tariff_plan = models.ForeignKey(ComboTariffPlan, verbose_name="Комбо-тариф",
                                          on_delete=models.DO_NOTHING, null=True, blank=True)
    state = models.CharField(verbose_name='Статус', choices=STATE_CHOICES, max_length=15)
    created_at = models.DateTimeField(auto_now=True, verbose_name="Дата заключения договора")

    class Meta:
        verbose_name = "Agreements"
        verbose_name_plural = "Договоры"
        ordering = ("user",)
