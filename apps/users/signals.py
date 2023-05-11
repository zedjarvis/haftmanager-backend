from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from notifications.signals import notify

User = get_user_model()

WELCOME_MESSAGE = "Welcome to Halfmanager! We're excited to have you on board and look forward to helping you manage your projects efficiently. If you have any questions or feedback, don't hesitate to reach out to our support team. Happy managing!"


@receiver(post_save, sender=User)
def user_welcome_message(sender, **kwargs):
    if kwargs.get("created", False):
        instance = kwargs.get("instance")
        notify.send(instance, recipient=instance, verb=WELCOME_MESSAGE)
