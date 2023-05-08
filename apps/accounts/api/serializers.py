from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField

from apps.accounts.models import Industry, Account, Phone, Email, AccountSettings


class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Industry
        fields = "__all__"


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = "__all__"


class PhoneSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField(region="KE")

    class Meta:
        model = Phone
        fields = "__all__"


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = "__all__"


class AccountSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountSettings
        fields = "__all__"
