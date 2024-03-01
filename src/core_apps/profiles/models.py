
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _ 

from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField 

from core_apps.common.models import TimeStampModel

User = get_user_model()

class Profile(TimeStampModel): 
        class Gender(models.TextChoices): 
                MALE = ('M', _('Male'))
                FEMALE = ('F', _('Female'))
                OTHER = ('O', _('Other'))

        user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
        profile_photo = models.ImageField(verbose_name=_('Profile Photo'), default='/default_profile_photo.png')
        gender = models.CharField(
                verbose_name = _('Gender'), 
                choices=Gender.choices, 
                default=Gender.MALE, 
                max_length=3
        )
        phone_number = PhoneNumberField(
                verbose_name=_('Phone Number'), max_length=20, default='+918513998991'
        )

        about_me = models.TextField(verbose_name=_('About Me'),  default='Say something about yourself')
        
        country = CountryField(verbose_name=_('Country'), default='IN', null=True, blank=True)
        city = models.CharField(verbose_name=_('City'), max_length=30, default='Kolkata', null=True, blank=True)
        
        twitter_handle = models.CharField(verbose_name=_('Twitter/X Handle'), max_length=25, blank=True)
        followers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)
        
        def follow(self, profile): 
                self.followers.add(profile)
        
        def unfollow(self, profile): 
                self.followers.remove(profile)
        
        def is_following(self, profile): 
                return self.followers.filter(pkid=profile.pkid).exists()

        
        def __str__(self): 
                return f"{self.user.first_name}'s Profile"
        
        