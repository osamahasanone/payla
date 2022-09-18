from django.contrib import admin
from django.urls import include, path
from rest_framework.schemas import get_schema_view

from core.views import read_docs

urlpatterns = [
    path("admin/", admin.site.urls),
    path("openapi", get_schema_view(title=""), name="openapi-schema"),
    path("docs", read_docs, name="docs"),
    path("newsletter/", include("newsletter.urls")),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
]
