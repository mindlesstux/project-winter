from django.contrib import admin
from .models import *

class DomainAdmin(admin.ModelAdmin):
    list_display = ["domain_name", "org_owner", "domain_date_created", "domain_date_updated", "domain_date_expiry"]
    list_filter = ["org_owner"]

# Register your models here.
admin.site.register(Domain, DomainAdmin)

