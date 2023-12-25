from django.contrib import admin
from django.contrib.auth.models import Group

from .models import MobileTariffPlan, User, HomeTariffPlan, ComboTariffPlan, Agreement, Account, BalanceChange, \
    OptionalEquipment


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_filter = ("is_staff",)
    fields = ["is_superuser", "first_name", "last_name", "is_staff", "is_active",
              "date_joined", "is_deleted", "deleted_at", "phone_number"]


@admin.register(MobileTariffPlan)
class MobileTariffPlanAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(HomeTariffPlan)
class HomeTariffPlanAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_filter = ("price",)


@admin.register(ComboTariffPlan)
class ComboTariffPlanAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_filter = ("price",)


@admin.register(Agreement)
class AgreementAdmin(admin.ModelAdmin):
    pass


@admin.register(BalanceChange)
class BalanceChangeAdmin(admin.ModelAdmin):
    pass


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    pass


@admin.register(OptionalEquipment)
class OptionalEquipmentAdmin(admin.ModelAdmin):
    list_filter = ("price",)


admin.site.site_header = "Администрирование RocketNet"
admin.site.site_title = "Панель администрирования"
admin.site.index_title = "Добро пожаловать в администрирование RocketNet"

admin.site.unregister(Group)
