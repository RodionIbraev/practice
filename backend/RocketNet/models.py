from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(max_length=128, verbose_name="Имя")
    phone_number = models.CharField(max_length=128, unique=True, verbose_name="Номер телефона")
    password = models.CharField(max_length=128, verbose_name="Пароль")
    username = None

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
