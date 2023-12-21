from django.contrib import admin
from django.contrib.auth.models import Group

from .models import MobileTariffPlan, User, HomeTariffPlan, ComboTariffPlan, Agreement

admin.site.register(User)
admin.site.register(MobileTariffPlan)
admin.site.register(HomeTariffPlan)
admin.site.register(ComboTariffPlan)
admin.site.register(Agreement)

admin.site.site_header = "Администрирование RocketNet"
admin.site.site_title = "Панель администрирования"
admin.site.index_title = "Добро пожаловать в администрирование RocketNet"

admin.site.unregister(Group)
