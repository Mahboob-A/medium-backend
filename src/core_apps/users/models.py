from django.db import models
import uuid 
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _ 

from .managers import CustomUserManager

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 16 digits allowed including country code.")

class CustomUser(AbstractBaseUser, PermissionsMixin): 
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    first_name = models.CharField(verbose_name=_("First Name"), max_length=50)
    last_name = models.CharField(verbose_name=_("Last Name"), max_length=50)
    email = models.EmailField(verbose_name=_("Email Address"), max_length=50, db_index=True, unique=True)
    user_image = models.ImageField(verbose_name=_("User Image Profile Picture"), upload_to='CustomUsers/UserImage/', default='CustomUsers/default-user-image.jpg', null=True, blank=True)
    phone_number = models.CharField(verbose_name=_("Phone Number"), max_length=16, validators=[phone_regex], unique=True, null=True, blank=True)

    is_active = models.BooleanField(verbose_name=_("Is Active"), default=True)
    is_staff = models.BooleanField(verbose_name=_("Is Staff"), default=False)

    otp = models.CharField(verbose_name=_("OTP"), max_length=6, null=True, blank=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at= models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta: 
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    @property
    def get_full_name(self):     
        return f"{self.first_name.title()} {self.last_name.title()}"
    
    @property
    def get_email(self): 
        return self.email
    
    @property
    def get_phone_number(self):
        return self.phone_number 
    
    def __str__(self):
        return f'{self.first_name.title()} {self.last_name.title()}'
    

