from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .serializers import UserSerializer, ProfileSerializer, SettingSerializer
from apps.users.models import User, Profile, Settings


# TODO: ADD permisson to check if isadmin or isself on change password action
class UserViewset(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class ProfileViewset(ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()


class SettingsViewset(ModelViewSet):
    serializer_class = SettingSerializer
    queryset = Settings.objects.all()
