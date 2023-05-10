from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField
from model_utils.models import TimeStampedModel, SoftDeletableModel
from imagekit.models import (
    ProcessedImageField,
)  # imagekit for processings images in django
from imagekit.processors import ResizeToFill

# Create your models here.


def account_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f"accounts/{instance.name}-{instance.pk}/{filename}"


class Industry(TimeStampedModel):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Industries"

    def __str__(self) -> str:
        return self.name


# different accounts[companies/individual]
class Account(TimeStampedModel, SoftDeletableModel):
    name = models.CharField(max_length=255)
    website = models.URLField(max_length=255)
    description = models.TextField(
        _("A short description of company or individual"), blank=True, null=True
    )
    billing_address = models.CharField(max_length=255, blank=True)
    shipping_address = models.CharField(max_length=255, blank=True)
    logo = ProcessedImageField(
        upload_to=account_directory_path,
        processors=[ResizeToFill(200, 200)],
        blank=True,
        null=True,
        format="JPEG",
        options={"quality": 80},
    )
    industry = models.ManyToManyField(Industry, blank=True)

    def __str__(self):
        return self.name


class Phone(TimeStampedModel):
    phone_number = PhoneNumberField(blank=True)
    is_primary = models.BooleanField(default=False)
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="phones"
    )

    class Meta:
        verbose_name = "Account Phone"
        constraints = [
            models.UniqueConstraint(
                fields=["account", "phone_number"], name="unique_account_phone_number"
            )
        ]

    def __str__(self) -> str:
        return self.number

    def clean(self) -> None:
        super().clean()
        # filter primary phone number
        primary_phones = self.account.phones.filter(is_primary=True).count()
        # raise a validation error if there is already a primary phone for this account
        if self.is_primary and primary_phones > 0:
            raise ValidationError("An account can only have one primary phone number")
        # raise a validation error if this account already has 2 phone numbers
        if not self.pk and self.account.phones.count() >= 2:
            raise ValidationError(
                "An account can only have a maximum on 2 phone numbers"
            )
        # if no primary phone, assign the first one
        if not self.pk and primary_phones == 0:
            self.is_primary = True

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class Email(TimeStampedModel, SoftDeletableModel):
    email_address = models.EmailField(max_length=255)
    is_primary = models.BooleanField(default=False)
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="emails"
    )

    class Meta:
        verbose_name = "Account Email"
        constraints = [
            models.UniqueConstraint(
                fields=["account", "email_address"], name="unique_account_email_address"
            )
        ]

    def __str__(self) -> str:
        return self.email_address

    def clean(self) -> None:
        super().clean()
        # filter primary email address
        primary_emails = self.account.emails.filter(is_primary=True).count()
        # raise a validation error if there is already a primary phone for this account
        if (
            self.is_primary and primary_emails > 0
        ):  # TODO: FIX THIS BUG(first check if email is being added before validating)
            raise ValidationError("An account can only have one primary email address")
        # raise a validation error if this account already has 2 email addresses
        if not self.pk and self.account.emails.count() >= 2:
            raise ValidationError(
                "An account can only have a maximum on 2 email addresses"
            )
        # if no primary email, assign the first one
        if not self.pk and primary_emails == 0:
            self.is_primary = True

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class AccountSettings(TimeStampedModel):
    account = models.OneToOneField(
        Account, on_delete=models.CASCADE, related_name="acount_settings"
    )
    currency = models.CharField(max_length=128, blank=True)
    time_zone = models.CharField(max_length=128, blank=True)

    class Meta:
        verbose_name_plural = "Account Settings"

    def __str__(self) -> str:
        return self.account.name
