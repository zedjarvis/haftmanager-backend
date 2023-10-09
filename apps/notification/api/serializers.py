from notifications.models import Notification
from rest_framework import serializers

from apps.users.api.serializers import UserSerializer


class NotificationSerializer(serializers.ModelSerializer):
    # actor = UserSerializer(required=False, allow_null=True)
    class Meta:
        model = Notification
        fields = [
            "id",
            "verb",
            "description",
            "level",
            "unread",
            "timestamp",
            "data",
            # "actor",
            # "action_object",
            # "target",
        ]
