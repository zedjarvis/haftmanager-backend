"""
URL configuration for core project.

"""
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView,
                                   SpectacularSwaggerView)

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # Optional UI:
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]


API_BASE = r"^api/v1/"
API_AUTH = r"^api/v1/auth/"

# API URLS
urlpatterns += [
    re_path(API_AUTH, include("rest_framework.urls")),
    re_path(API_AUTH, include("djoser.urls")),
    re_path(API_AUTH, include("djoser.urls.jwt")),
    re_path(API_BASE, include("core.api_router")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
