from django.db.models.query import QuerySet
from rest_framework import status  # noqa: F401
from rest_framework.decorators import action  # noqa: F401
from rest_framework.response import Response  # noqa: F401
from rest_framework.viewsets import ModelViewSet

from .serializers import Notification, NotificationSerializer


class NotificationViewset(ModelViewSet):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()

    def get_queryset(self) -> QuerySet:
        user = self.get_instance()
        qs = super().get_queryset()
        return qs.filter(recipient=user, deleted=False, public=True)

    def get_instance(self):
        return self.request.user
