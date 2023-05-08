from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .serializers import (
    IndustrySerializer,
    AccountSerializer,
    PhoneSerializer,
    EmailSerializer,
    AccountSettingsSerializer,
)

from apps.accounts.models import Industry, Account, Phone, Email, AccountSettings


class IndustryViewset(ModelViewSet):
    serializer_class = IndustrySerializer
    queryset = Industry.objects.all()


class AccountViewset(ModelViewSet):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()


class PhoneViewset(ModelViewSet):
    serializer_class = PhoneSerializer
    queryset = Phone.objects.all()


class EmailViewset(ModelViewSet):
    serializer_class = EmailSerializer
    queryset = Email.objects.all()


class AccountSettingsViewset(ModelViewSet):
    serializer_class = AccountSettingsSerializer
    queryset = AccountSettings.objects.all()
