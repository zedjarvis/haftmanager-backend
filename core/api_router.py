from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from apps.accounts.api import views as AccountViews

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

# Account viewsets
router.register("industries", AccountViews.IndustryViewset)
router.register("accounts", AccountViews.AccountViewset)
router.register("phone_numbers", AccountViews.PhoneViewset)
router.register("email_addresses", AccountViews.EmailViewset)
router.register("account_settings", AccountViews.AccountSettingsViewset)

app_name = "api"
urlpatterns = router.urls
