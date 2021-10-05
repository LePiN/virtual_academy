from django.contrib import admin
from django.urls import include
from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="E-academyI",
        default_version="v1",
        description="E-academy documentation.",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("api/v1/", include("api.urls")),
    path("admin/", admin.site.urls),
    path("docs/", schema_view.with_ui("swagger", cache_timeout=0)),
]
