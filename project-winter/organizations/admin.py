from django.contrib import admin
from .models import *

class StreetAddressAdmin(admin.ModelAdmin):
    list_display = ["address_line_1", "address_line_2", "city", "state_province", "postal_code", "country"]
    list_filter = ["country", "state_province"]

class ContactAdmin(admin.ModelAdmin):
    list_display = ["contact_first_name", "contact_last_name", "contact_title", "contact_department", "contact_phone_desk", "contact_phone_mobile", "contact_phone_fax", "user"]
    #list_filter = [""]

# Register your models here.
admin.site.register(Organization)
admin.site.register(Contact, ContactAdmin)
admin.site.register(StreetAddress, StreetAddressAdmin)
