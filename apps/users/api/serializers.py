from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField

from apps.users.models import User, Profile, Settings


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "last_login"]


class ProfileSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField(region="KE")

    class Meta:
        model = Profile
        fields = "__all__"


class SettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settings
        fields = "__all__"
