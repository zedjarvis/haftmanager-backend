from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from imagekit.models import (
    ProcessedImageField,
)  # imagekit for processings images in django
from imagekit.processors import ResizeToFill
from model_utils import Choices
from model_utils.fields import StatusField
from model_utils.models import SoftDeletableModel, TimeStampedModel
from phonenumber_field.modelfields import PhoneNumberField

from apps.accounts.models import Account
from apps.users.managers import UserManager


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f"users/user-{instance.pk}/{filename}"


class User(AbstractUser, TimeStampedModel, SoftDeletableModel):
    """
    Default custom user model for haftmanager-backend.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    first_name = models.CharField(_("First Name of User"), blank=True, max_length=255)
    last_name = models.CharField(_("Last Name of User"), blank=True, max_length=255)
    email = models.EmailField(_("Email address"), unique=True)
    username = None  # type: ignore
    account = models.ForeignKey(
        Account, on_delete=models.SET_NULL, blank=True, null=True, related_name="users"
    )
    created_by = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="users_created",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Profile(TimeStampedModel, SoftDeletableModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone_number = PhoneNumberField(blank=True)
    address = models.CharField(max_length=255, blank=True)
    avatar = ProcessedImageField(
        upload_to=user_directory_path,
        processors=[ResizeToFill(200, 200)],
        blank=True,
        null=True,
        format="JPEG",
        options={"quality": 80},
    )

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def __str__(self) -> str:
        return self.user.email


class Settings(TimeStampedModel):
    THEMES = Choices("dark", "light")

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="settings")
    theme = StatusField(choices_name="THEMES", default="dark")

    class Meta:
        verbose_name = "User Setting"
        verbose_name_plural = "User Settings"

    def __str__(self) -> str:
        return self.user.email
