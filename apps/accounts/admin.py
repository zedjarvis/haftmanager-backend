from django.contrib import admin

# Register your models here.
from apps.accounts.models import Industry, Account, Phone, Email, AccountSettings

admin.site.register(Industry)
admin.site.register(Account)
admin.site.register(Phone)
admin.site.register(Email)
admin.site.register(AccountSettings)
