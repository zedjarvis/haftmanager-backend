from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from apps.accounts.api import views as AccountViews
from apps.notification.api import views as NotificationViews
from apps.users.api import views as UserViews

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

# Account viewsets
router.register("accounts", AccountViews.AccountViewset)
router.register("account_settings", AccountViews.AccountSettingsViewset)
router.register("account_industries", AccountViews.IndustryViewset)
router.register("account_phones", AccountViews.PhoneViewset)
router.register("account_emails", AccountViews.EmailViewset)

# Users viewsets
router.register("users", UserViews.UserViewset)
router.register("user_profiles", UserViews.UserProfileViewset)
router.register("user_settings", UserViews.UserSettingsViewset)

# Notification viewsets
router.register("notifications", NotificationViews.NotificationViewset)


app_name = "api"
urlpatterns = router.urls
