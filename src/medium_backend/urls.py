"""medium_backend URL Configuration """



from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from drf_yasg import openapi 
from drf_yasg.views import get_schema_view
from rest_framework import permissions

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

urlpatterns = [
    path('redoc/', doc_schema_view.with_ui("redoc", cache_timeout=0)),
    path(settings.ADMIN_URL, admin.site.urls),

]


admin.site.site_header = "Medium Backend API"
admin.site.site_title = "Medium Backend Admin Portal"
admin.site.index_title = "Welcome to Medium Backend API Portal"
