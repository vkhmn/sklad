from django.contrib import admin

from app.contactor.models import BankDetails, Vendor, Person, Buyer


@admin.register(BankDetails)
class BankDetailsAdmin(admin.ModelAdmin):
    pass


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    pass


@admin.register(Buyer)
class VendorAdmin(admin.ModelAdmin):
    pass


@admin.register(Person)
class VendorAdmin(admin.ModelAdmin):
    pass
