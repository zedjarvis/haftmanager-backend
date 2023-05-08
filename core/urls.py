"""
URL configuration for core project.

"""
from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
]

API_AUTH = r"^api/auth"
API_BASE = r"^api/v1/"

urlpatterns += [
    re_path(API_AUTH, include("rest_framework.urls")),
    re_path(API_AUTH, include("djoser.urls")),
    re_path(API_AUTH, include("djoser.urls.jwt")),
    re_path(API_BASE, include("core.api_router")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
