from django.contrib import admin

from .models import BankDetails, Vendor


@admin.register(BankDetails)
class BankDetailsAdmin(admin.ModelAdmin):
    pass


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    pass
