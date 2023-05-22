from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Account, AccountSettings

# TODO: SAVE SIGNALS FROM PHONE, EMAIL AND SETTINGS TRIGGER NOTIFICATIONS:


@receiver(post_save, sender=Account)
def create_account_settings(sender, instance, created, **kwargs):
    if created:
        AccountSettings.objects.create(account=instance)


@receiver(post_save, sender=Account)
def save_account_settings(sender, instance, **kwargs):
    instance.account_settings.save()
