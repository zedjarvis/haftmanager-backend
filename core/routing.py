from django.urls import re_path
import apps.notification.consumers as NotifConsumers

websocket_urlpatterns = [
    re_path(r"^ws/notifications/$", NotifConsumers.NotificationConsumer.as_asgi())
]

