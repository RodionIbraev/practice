from django.contrib import admin

from .models import MobileTariffPlan, User, HomeTariffPlan, ComboTariffPlan, Agreement

admin.site.register(User)
admin.site.register(MobileTariffPlan)
admin.site.register(HomeTariffPlan)
admin.site.register(ComboTariffPlan)
admin.site.register(Agreement)
