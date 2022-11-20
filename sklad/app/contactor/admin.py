from django.contrib import admin

from app.contactor.models import BankDetails, Vendor, Person, Buyer


@admin.register(BankDetails)
class BankDetailsAdmin(admin.ModelAdmin):
    list_display = ['pk', 'bank_name', 'account']
    list_editable = ['bank_name', 'account']
    list_filter = ['bank_name']


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'address', 'contact_person', 'bank_details']
    list_editable = ['name', 'address', 'contact_person', 'bank_details']


@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    list_display = ['get_name', 'get_email', 'get_phone']

    def get_name(self, object):
        return object.person.full_name

    get_name.short_description = 'Имя'

    def get_email(self, object):
        return object.person.email

    get_email.short_description = 'Email'

    def get_phone(self, object):
        return object.person.phone

    get_phone.short_description = 'Телефон'


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['pk', 'full_name', 'email', 'phone']
    list_editable = ['full_name', 'email', 'phone']
