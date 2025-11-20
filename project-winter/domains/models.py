import uuid
from django.db import models
from django.utils import timezone
from organizations.models import *


# Create your models here.
class Domain(models.Model):
    domain_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    domain_name = models.CharField(max_length=255)
    org_owner = models.ForeignKey(Organization, on_delete=models.RESTRICT, null=True, blank=True)
    domain_date_created = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    domain_date_updated = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    domain_date_expiry = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    domain_name_servers = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return self.domain_name

    class Meta:
        verbose_name = "Domain"
        verbose_name_plural = "Domains"