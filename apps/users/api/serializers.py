from django.db import transaction, IntegrityError
from django.contrib.auth.tokens import default_token_generator
from django.utils.translation import gettext_lazy as _
from djoser.serializers import PasswordRetypeSerializer
from rest_framework import serializers, exceptions
from rest_framework.exceptions import ValidationError
from rest_framework_recursive.fields import RecursiveField
from phonenumber_field.serializerfields import PhoneNumberField

from djoser import utils

from apps.users.models import User, Profile, Settings


class ProfileSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField(region="KE")

    class Meta:
        model = Profile
        fields = [
            "id",
            "phone_number",
            "address",
            "avatar",
        ]


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False, allow_null=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "created_by",
            "profile",
        ]
        read_only_fields = ("id", "created_by")


class InviteUserMixin:
    def create(self, validated_data):
        try:
            user = self.perform_create(validated_data)
        except IntegrityError as e:
            raise serializers.ValidationError(e)
        return user

    def perform_create(self, validated_data):
        """
        Invited users are created with is_active=False and no password.
        User sets password on account activation.
        """
        user_account = validated_data.pop("user_accounts")
        # TODO: ADD PROJECTS M2M RELATIONSHIP
        # TODO: USE CELERY TO SEND EMAILS AND NOTIFICATIONS
        with transaction.atomic():
            user = User.objects.create_user(**validated_data)
            
        user.user_accounts.set(user_account)
        
        return user


class InviteUserSerializer(InviteUserMixin, serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "created_by",
            "user_accounts",
        ]


class UidAndTokenSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()

    default_error_messages = {
        "invalid_token": _("Invalid token for given user."),
        "invalid_uid": _("Invalid user id or user doesn't exist."),
    }

    def validate(self, attrs):
        validated_data = super().validate(attrs)

        # uid validation have to be here, because validate_<field_name>
        # doesn't work with modelserializer
        try:
            uid = utils.decode_uid(self.initial_data.get("uid", ""))
            self.user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            key_error = "invalid_uid"
            raise ValidationError(
                {"uid": [self.error_messages[key_error]]}, code=key_error
            )

        is_token_valid = default_token_generator.check_token(
            self.user, self.initial_data.get("token", "")
        )
        if is_token_valid:
            return validated_data
        else:
            key_error = "invalid_token"
            raise ValidationError(
                {"token": [self.error_messages[key_error]]}, code=key_error
            )



class InviteUserActivationSerializer(UidAndTokenSerializer, PasswordRetypeSerializer):
    """Invited users need to activate their account and set password."""

    pass


class SettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settings
        fields = "__all__"
