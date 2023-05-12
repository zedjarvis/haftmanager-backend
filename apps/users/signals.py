from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from djoser.signals import user_activated
from notifications.signals import notify

from apps.users.models import Profile, Settings

User = get_user_model()

WELCOME_MESSAGE = (
    "Welcome to Halfmanager! We're excited to have you on board and "
    "look forward to helping you manage your projects efficiently. "
    "If you have any questions or feedback, don't hesitate to reach "
    "out to our support team. Happy managing!"
)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=User)
def create_user_settings(sender, instance, created, **kwargs):
    if created:
        Settings.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_settings(sender, instance, **kwargs):
    instance.settings.save()


@receiver(post_save, sender=User)
def user_welcome_message(sender, **kwargs):
    if kwargs.get("created", False):
        instance = kwargs.get("instance")
        notify.send(instance, recipient=instance, verb=WELCOME_MESSAGE, level="success")


@receiver(user_activated)
def user_welcome_email(sender, user, request, **kwargs):
    subject = "Welcome to Haft Manager App!"
    from_email = settings.EMAIL_HOST_USER
    to_email = user.email
    text_content = render_to_string("welcome_email.txt", {"user": user})
    html_content = render_to_string("welcome_email.html", {"user": user})
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, "text/html")
    msg.send(fail_silently=False)
