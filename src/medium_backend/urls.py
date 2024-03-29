"""medium_backend URL Configuration """


from dj_rest_auth import registration, urls
from dj_rest_auth.views import PasswordResetConfirmView
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from core_apps.users.views import CustomUserDetailsView, CustomUserDetailsView2

# documentation
doc_schema_view = get_schema_view(
    openapi.Info(
        title="Medium Backend API",
        default_version="v1.0",
        description="API Endpoints for Medium Backend",
        contact=openapi.Contact(email="iammahboob.a@gmail.com"),
        license=openapi.License(name="MIT Licence"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# urlpatterns

urlpatterns = [
    path("redoc/", doc_schema_view.with_ui("redoc", cache_timeout=0)),
    path(settings.ADMIN_URL, admin.site.urls),
    # Registration and Password reset urls | V1
    path("api/v1/auth/", include("dj_rest_auth.urls")),
    path("api/v1/auth/registration/", include("dj_rest_auth.registration.urls")),
    path(
        "api/v1/auth/password/reset/confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "api/v1/auth/user-details/",
        CustomUserDetailsView.as_view(),
        name="user_details",
    ),
    # profile app
    path("api/v1/profiles/", include("core_apps.profiles.urls")),
    # articles app
    path("api/v1/articles/", include("core_apps.articles.urls")),
    # ratings app
    path("api/v1/ratings/", include("core_apps.ratings.urls")),
    # bookmarks app
    path("api/v1/bookmarks/", include("core_apps.bookmarks.urls")),
    # responses app
    path("api/v1/responses/", include("core_apps.responses.urls")),
    # searches app (elastic search)
    path("api/v1/es/", include("core_apps.searches.urls")),
]


admin.site.site_header = "Medium Backend API"
admin.site.site_title = "Medium Backend Admin Portal"
admin.site.index_title = "Welcome to Medium Backend API Portal"
