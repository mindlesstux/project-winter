import uuid
from django.contrib.auth.models import User
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class StreetAddress(models.Model):
    # A model to store comprehensive street address information.

    # Street Details
    # You might consider making some of these fields optional (nullable=True)
    # depending on your specific requirements (e.g., for very simple addresses)

    address_line_1 = models.CharField(
        max_length=100,
        verbose_name="Address Line 1",
        help_text="Street name and building/house number (e.g., 123 Main St)"
    )
    address_line_2 = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Address Line 2",
        help_text="Apartment, suite, or box number (optional)"
    )

    # Geographic Details
    city = models.CharField(
        max_length=100
    )
    state_province = models.CharField(
        max_length=100,
        verbose_name="State/Province"
    )
    postal_code = models.CharField(
        max_length=20,
        verbose_name="Postal Code"
    )
    country = models.CharField(
        max_length=100,
        default="United States", # Set a sensible default if most addresses are in one country
        help_text="Country name"
    )

    # Optional: Geocoding fields (for storing latitude and longitude)
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name_plural = "Street Addresses"
        # Adding constraints or indexes might be beneficial for performance
        # e.g., unique_together = ('address_line_1', 'city', 'postal_code')

    def __str__(self):
        """String representation of the address for display/admin."""
        parts = [self.address_line_1]
        if self.address_line_2:
            parts.append(self.address_line_2)
        parts.extend([self.city, self.state_province, self.postal_code, self.country])
        return ", ".join(filter(None, parts))

    def full_address_display(self):
        """Returns a multi-line formatted address."""
        lines = [self.address_line_1]
        if self.address_line_2:
            lines.append(self.address_line_2)
        lines.append(f"{self.city}, {self.state_province} {self.postal_code}")
        lines.append(self.country)
        return "\n".join(lines)

# Create your models here.
class Organization(models.Model):
    org_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    org_name = models.CharField()
    org_url = models.URLField(null=True, blank=True)
    org_address = models.ForeignKey(StreetAddress, on_delete=models.RESTRICT, null=True, blank=True)
    org_parent = models.ForeignKey("self", on_delete=models.RESTRICT, null=True, blank=True)

    class Meta:
        verbose_name = "Organization"
        verbose_name_plural = "Organizations"

    def __str__(self):
        """Return the org name"""
        return f"{self.org_name}"

class Contact(models.Model):
    contact_uuid = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owned_contacts',
        null=True, blank=True
    )
    contact_first_name = models.CharField(
        verbose_name="First Name",
        help_text="First Name"
    )
    contact_last_name = models.CharField(
        verbose_name="Last Name",
        help_text="Last Name",
        null=True, blank=True
    )
    contact_title = models.CharField(
        verbose_name="Title",
        help_text="Title/Position",
        null=True, blank=True
    )
    contact_department = models.CharField(
        verbose_name="Deparment",
        help_text="Deparment within the organization",
        null=True, blank=True
    )
    contact_email = models.EmailField(
        verbose_name="E-Mail",
        help_text="E-Mail Address",
        null=True, blank=True
    )
    contact_phone_desk = PhoneNumberField(
        unique=True,
        region='US', # Optional: Set a default country region
        verbose_name="Desk Phone Number",
        help_text="Title/Position",
        blank=True
    )
    contact_phone_mobile = PhoneNumberField(
        unique=True,
        region='US', # Optional: Set a default country region
        verbose_name="Mobile Phone Number",
        blank=True
    )
    contact_phone_fax = PhoneNumberField(
        unique=True,
        region='US', # Optional: Set a default country region
        verbose_name="Fax Phone Number",
        blank=True
    )

    contact_organizations = models.ManyToManyField(
        Organization,
        related_name='contacts', # The name used to look up contacts from an organization
        blank=True,             # Allows a contact to be saved without any organizations
        help_text="The organizations this contact is associated with."
    )

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"

    def __str__(self):
        return f"{self.contact_first_name} {self.contact_last_name}"