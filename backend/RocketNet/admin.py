from django.contrib import admin
from django.contrib.auth.models import Group

from .models import MobileTariffPlan, User, HomeTariffPlan, ComboTariffPlan, Agreement


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(MobileTariffPlan)
class MobileTariffPlanAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(HomeTariffPlan)
class HomeTariffPlanAdmin(admin.ModelAdmin):
    search_fields = ("name", )


@admin.register(ComboTariffPlan)
class ComboTariffPlanAdmin(admin.ModelAdmin):
    search_fields = ("name", )
    list_filter = ("price", )


@admin.register(Agreement)
class AgreementAdmin(admin.ModelAdmin):
    list_filter = ("state", )


admin.site.site_header = "Администрирование RocketNet"
admin.site.site_title = "Панель администрирования"
admin.site.index_title = "Добро пожаловать в администрирование RocketNet"

admin.site.unregister(Group)
