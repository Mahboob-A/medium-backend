
# django 
from django.contrib.auth import get_user_model

# drf 
from rest_framework import serializers

# allauth
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email

# dj rest auth 
from dj_rest_auth.registration.serializers import RegisterSerializer

# others 
from django_countries.serializer_fields import CountryField
from phonenumber_field.serializerfields import PhoneNumberField

from core_apps.profiles.models import Profile
from core_apps.profiles.serializer import UserDetailsProfileSerializer


User = get_user_model()


class UserSerializer(serializers.ModelSerializer): 
        ''' Serializer for User '''
        profile_id = serializers.UUIDField(source='profile.id')
        gender = serializers.CharField(source="profile.gender")
        phone_number = PhoneNumberField(source="profile.phone_number")
        profile_photo = serializers.ReadOnlyField(source="profile.profile_photo.url")
        country = CountryField(source="profile.country")
        city = serializers.CharField(source="profile.city")
        twitter_handle = serializers.CharField(source="profile.twitter_handle")
        total_followers = serializers.SerializerMethodField(read_only=True)
        
        class Meta: 
                model = User
                fields = ['id', 'profile_id', 'email', 'first_name', 'last_name', 'gender', 'phone_number', 'profile_photo', 'country', 'city', 'twitter_handle', 'total_followers']

        def get_total_followers(self, obj): 
                return obj.profile.followers.all()

        def to_representation(self, instance):
                representation =  super(UserSerializer, self).to_representation(instance)

                if instance.is_superuser: 
                        representation['admin'] = True 
                return representation


class CustomRegisterSerializer(RegisterSerializer): 
        username = None 
        first_name = serializers.CharField(required=True)
        last_name = serializers.CharField(required=True)
        email = serializers.EmailField(required=True)
        password1 = serializers.CharField(write_only=True)
        password2 = serializers.CharField(write_only=True)


        def get_cleaned_data(self):
                super().get_cleaned_data()     
                return {
                        'email': self.validated_data.get('email', ''), 
                        'first_name': self.validated_data.get('first_name', ''), 
                        'last_name': self.validated_data.get('last_name', ''), 
                        'password1': self.validated_data.get('password1', ''), 
                } 


        def save(self, request):
                adapter = get_adapter()
                user = adapter.new_user(request)
                self.cleaned_data = self.get_cleaned_data()
                user = adapter.save_user(request, user, self)
                
                user.save()
                
                setup_user_email(request, user, [])
                user.first_name = self.cleaned_data.get('first_name')
                user.last_name = self.cleaned_data.get('last_name')
                
                user.email = self.cleaned_data.get('email')

                user.password = self.cleaned_data.get('password1')
                
                return user 