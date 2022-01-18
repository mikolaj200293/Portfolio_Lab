from django.contrib import admin
from main.models import Category, Institution, Donation


class CategoryAdmin(admin.ModelAdmin):
    pass


class InstitutionAdmin(admin.ModelAdmin):
    pass


class DonationAdmin(admin.ModelAdmin):
    pass


admin.site.register(Category, CategoryAdmin)
admin.site.register(Institution, InstitutionAdmin)
admin.site.register(Donation, DonationAdmin)


