
from django_countries.serializer_fields import CountryField
from rest_framework import serializers

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer): 
        ''' Profile serializer - serializes few User fields also along with general Profile fields  '''
        first_name = serializers.CharField(source='user.first_name')
        last_name = serializers.CharField(source='user.last_name')
        email = serializers.EmailField(source='user.email')
        full_name = serializers.SerializerMethodField(read_only=True)
        profile_photo = serializers.SerializerMethodField()
        country = CountryField(name_only=True)
        
        class Meta: 
                model = Profile
                fields = [
                        'id', 'first_name', 'last_name', 'email', 'profile_picture', 'country', 'city', 'phone_number', 'gender', 'about_me', 'twitter_handle'         
                ]

        def get_full_name(self, obj):
                return obj.user.get_full_name()

        def get_profile_photo(self, obj):
                return obj.profile_photo.url 
        
        

class ProfileUpdateSerializer(serializers.ModelSerializer): 
        ''' Update the Profile details of user '''
        country = CountryField(name_only=True)
        
        class Meta: 
                model = Profile 
                fields = ['first_name', 'last_name', 'full_name', 'gender', 'twitter_handle', 'phone_number', 'profile_photo', 'country', 'city', 'about_me']


class UserFollowingSerializer(serializers.ModelSerializer): 
        ''' Follower of the currently logged in user '''
        first_name = serializers.CharField(source='user.first_name')
        last_name = serializers.CharField(source='user.last_name')
        country = CountryField(name_only=True)
        
        class Meta: 
                model = Profile
                fields = ['first_name', 'last_name', 'profile_photo', 'about_me', 'twitter_handle',  'country', 'city']

























