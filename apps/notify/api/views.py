from rest_framework.viewsets import ModelViewSet

from .serializers import NotificationSerializer, Notification


class NotificationViewset(ModelViewSet):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()
