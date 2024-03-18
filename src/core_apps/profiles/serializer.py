from django_countries.serializer_fields import CountryField
from rest_framework import serializers

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """Profile serializer - serializes few User fields also along with general Profile fields"""

    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.EmailField(source="user.email")
    full_name = serializers.SerializerMethodField(read_only=True)
    profile_photo = serializers.SerializerMethodField()
    country = CountryField(name_only=True)
    profile_id = serializers.SerializerMethodField(read_only=True)
    user_id = serializers.UUIDField(source="user.id", read_only=True)
    total_followers = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = [
            "profile_id",
            "user_id",
            "first_name",
            "last_name",
            "full_name",
            "email",
            "profile_photo",
            "country",
            "city",
            "phone_number",
            "gender",
            "about_me",
            "twitter_handle",
            "total_followers",
        ]

    def get_profile_id(self, obj):
        return str(obj.id)

    def get_full_name(self, obj):
        first_name = obj.user.first_name
        last_name = obj.user.last_name
        return f"{first_name.title()} {last_name.title()}"

    def get_profile_photo(self, obj):
        return obj.profile_photo.url

    def get_total_followers(self, obj):
        return obj.followers.all().count()


class ProfileUpdateSerializer(serializers.ModelSerializer):
    """Update the Profile details of user"""

    country = CountryField(name_only=True)

    class Meta:
        model = Profile
        fields = [
            "gender",
            "twitter_handle",
            "phone_number",
            "profile_photo",
            "country",
            "city",
            "about_me",
        ]


class UserFollowerAndFollowingSerializer(serializers.ModelSerializer):
    """Follower of the currently logged in user"""

    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    country = CountryField(name_only=True)

    class Meta:
        model = Profile
        fields = [
            "first_name",
            "last_name",
            "profile_photo",
            "about_me",
            "twitter_handle",
            "country",
            "city",
        ]


class UserDetailsProfileSerializer(serializers.ModelSerializer):
    """Profile Serializer for serializing Profile of an User while fetching User Details"""

    country = CountryField(read_only=True)
    total_followers = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = [
            "gender",
            "twitter_handle",
            "phone_number",
            "profile_photo",
            "country",
            "city",
            "about_me",
            "total_followers",
        ]

    def get_total_followers(self, obj):
        return obj.followers.all()
