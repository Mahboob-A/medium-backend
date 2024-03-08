from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _ 

from .forms import UserChangeForm, UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

@admin.register(User)
class UserAdminClass(BaseUserAdmin):
    ordering = ['email']
    form = UserChangeForm
    add_form = UserCreationForm
    
    model = User 
    list_display = ['pkid', 'id', 'first_name', 'last_name', 'email', 'phone_number', 'is_staff', 'is_active']

    list_display_links = ['pkid', 'id', 'email']

    list_filter = ['email', 'is_staff', 'is_active']

    fieldsets = (
        (_("Login Credentials"), {"fields": ("email", "password")}),
        (_("User Information"), {"fields": ("first_name", "last_name", "user_image", "phone_number")}),
        (_("Permissions and Groups"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        (_("Events"), {"fields": ("created_at", )}),
        #(_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    
    add_fieldsets = (
        (None, {
            "classes": ("wide",), 
            "fields": ("email", "first_name", "last_name", "password1", "password2"), 
        }),
    )


    search_fields = ["email", "first_name", "last_name"]







