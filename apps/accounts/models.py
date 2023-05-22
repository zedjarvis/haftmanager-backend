from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from model_utils.models import SoftDeletableModel, TimeStampedModel
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

User = get_user_model()


def account_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f"accounts/{instance.name}-{instance.pk}/{filename}"


class Industry(TimeStampedModel, SoftDeletableModel):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Industries"

    def __str__(self) -> str:
        return self.name


# different accounts[companies/individual]
class Account(TimeStampedModel, SoftDeletableModel):
    name = models.CharField(_("Name of Company or Individual"), max_length=255)
    website = models.URLField(_("Your Website"), max_length=255)
    description = models.TextField(
        _("A short description of company or individual"), blank=True, null=True
    )
    billing_address = models.CharField(_("Billing Address"), max_length=255, blank=True)
    shipping_address = models.CharField(
        _("Shipping Address"), max_length=255, blank=True
    )
    logo = ProcessedImageField(
        upload_to=account_directory_path,
        processors=[ResizeToFill(200, 200)],
        blank=True,
        null=True,
        format="JPEG",
        options={"quality": 80},
    )
    industry = models.ManyToManyField(Industry, blank=True, related_name="accounts")
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="accounts_created",
    )
    users = models.ManyToManyField(User, blank=True, related_name="account")

    def __str__(self):
        return self.name


# TODO : add created_by and modified_by fields to both phone and email models
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
        return f"{self.phone_number}"

    def clean(self) -> None:
        super().clean()
        # filter primary phone number
        primary_phones = self.account.phones.filter(is_primary=True).count()

        if not self.pk:
            account_phones = self.account.phones.count()
            # raise a validation error if this account already has 2 phone numbers
            if account_phones >= 2:
                raise ValidationError(
                    "An account can only have a maximum of 2 phone numbers"
                )
            # raise a validation error if there is already a primary phone for this account
            if self.is_primary and primary_phones > 0:
                raise ValidationError(
                    "An account can only have one primary phone number"
                )

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
        if not self.pk:
            account_emails = self.account.emails.count()
            # raise a validation error if this account already has 2 phone numbers
            if account_emails >= 2:
                raise ValidationError(
                    "An account can only have a maximum of 2 email addresses."
                )
            # raise a validation error if there is already a primary phone for this account
            if self.is_primary and primary_emails > 0:
                raise ValidationError(
                    "An account can only have one primary eamil adress."
                )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class AccountSettings(TimeStampedModel):
    account = models.OneToOneField(
        Account, on_delete=models.CASCADE, related_name="account_settings"
    )
    currency = models.CharField(_("Currency"), max_length=128, blank=True)
    time_zone = models.CharField(_("Time Zone"), max_length=128, blank=True)

    class Meta:
        verbose_name_plural = "Account Settings"

    def __str__(self) -> str:
        return self.account.name
