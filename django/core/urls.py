from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("home.urls", namespace="restaurant")),
    path("api/v0/", include("api.urls", namespace="api")),
]
