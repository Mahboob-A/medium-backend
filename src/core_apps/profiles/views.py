from django.shortcuts import render

# Create your views here.
# TODO change the .dev into production in Production
from medium_backend.settings.dev import DEFAULT_FROM_EMAIL

# django
from django.core.mail import send_mail
from django.contrib.auth import get_user_model

# drf
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser  # for file uploads
from rest_framework import generics, status

# local
from .exception import CanNotFollowYouself
from .pagination import ProfilePagination
from .models import Profile
from .renderers import ProfileJSONRenderer, ProfilesJSONRenderer
from .serializer import (
    ProfileUpdateSerializer,
    ProfileSerializer,
    UserFollowerAndFollowingSerializer,
)


User = get_user_model()


class ProfileListAPIView(generics.ListAPIView):
    """API for listing all the user profiles"""

    queryset = Profile.objects.all()
    pagination_class = ProfilePagination
    serializer_class = ProfileSerializer
    renderer_classes = [ProfilesJSONRenderer]


class ProfileDetailAPIView(generics.RetrieveAPIView):
    """API for user profile details"""

    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer
    renderer_classes = [ProfileJSONRenderer]

    def get_queryset(self):
        queryset = Profile.objects.select_related("user")
        return queryset

    def get_object(self):
        user = self.request.user
        profile = self.get_queryset().get(user=user)
        return profile

        # as profile as one to one with user
        # return self.request.user.profile


class ProfileUpdateAPIView(generics.UpdateAPIView):
    """API for updating user profile"""

    serializer_class = ProfileUpdateSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]
    renderer_classes = [ProfileJSONRenderer]

    def get_object(self):
        return self.request.user.profile

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserFollowerAPIView(APIView):
    """API for all the followers of the currently logged in user"""

    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            # user_profile = Profile.objects.get(user__id=request.user.id)
            user_profile = self.request.user.profile
            all_follower_profiles = user_profile.followers.all()
            serializer = UserFollowerAndFollowingSerializer(
                all_follower_profiles, many=True
            )

            response_data = {
                "status_code": status.HTTP_200_OK,
                "follower_count": all_follower_profiles.count(),
                "followers": serializer.data,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        # technically the control would not reach here as Profile object is created using Signals whenever an User object is created.
        except Profile.DoesNotExist:
            return Response(
                {"message": "User has no followers"}, status=status.HTTP_404_NOT_FOUND
            )


class UserFollowingAPIView(APIView):
    """API for all the profiles the currently logged in user is following"""

    def get(self, request, format=None):
        try:
            user_profile = self.request.user.profile
            all_following_profiles = user_profile.following.all()
            serializer = UserFollowerAndFollowingSerializer(
                all_following_profiles, many=True
            )
            response_data = {
                "status_code": status.HTTP_200_OK,
                "following_count": all_following_profiles.count(),
                "following": serializer.data,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response(
                {"message": "User does not follow anyone"},
                status=status.HTTP_404_NOT_FOUND,
            )


class FollowAUserAPIView(APIView):
    """API for currently logged in user to follow another user_id (uuid)"""

    def post(self, requet, user_id, format=None):
        try:
            # user_profile = Profile.objects.get(user=self.request.user)
            user_profile = self.request.user.profile

            # user_id is  the user who is being followed by the currently logged in user.
            to_be_followed_profile = Profile.objects.get(user__id=user_id)

            if user_profile == to_be_followed_profile:
                raise CanNotFollowYouself()

            if user_profile.is_following_a_user(to_be_followed_profile):
                response_data = {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": f"You are already following {to_be_followed_profile.user.first_name.title()} {to_be_followed_profile.user.last_name.title()}",
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            # currently logged in user is following the user_id
            user_profile.follow_user(to_be_followed_profile)

            subject = "A New Follower for You!"

            message = f"""Hello {to_be_followed_profile.user.first_name.title()} {to_be_followed_profile.user.last_name.title()}! \n
                        {user_profile.user.first_name.title()} {user_profile.user.last_name.title()} is now following you! """

            from_email = DEFAULT_FROM_EMAIL
            recipient_list = [to_be_followed_profile.user.email]
            send_mail(
                subject=subject,
                message=message,
                from_email=from_email,
                recipient_list=recipient_list,
                fail_silently=True,
            )

            response_data = {
                "status_code": status.HTTP_200_OK,
                "message": f"You are now following {to_be_followed_profile.user.first_name.title()} {to_be_followed_profile.user.last_name.title()}!",
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except Profile.DoesNotExist:
            raise NotFound("You can not follow a user that does not exist!")


class UnfollowAUserAPIView(APIView):
    """API for unfollwing a user_id by currently logged in user"""

    def post(self, request, user_id, format=None):
        try:
            user_profile = self.request.user.profile
            to_be_unfollowed_profile = Profile.objects.get(user__id=user_id)

            if not user_profile.is_following_a_user(to_be_unfollowed_profile):
                response_data = {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": f"You can not unfollow as you are not following {to_be_unfollowed_profile.user.first_name.title()} {to_be_unfollowed_profile.user.last_name.title()}",
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            user_profile.unfollow_user(to_be_unfollowed_profile)
            response_data = {
                "status_code": status.HTTP_200_OK,
                "message": f"You have unfollowed {to_be_unfollowed_profile.user.first_name.title()} {to_be_unfollowed_profile.user.last_name.title()}!",
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except Profile.DoesNotExist:
            raise NotFound("You can not unfollow a user that does not exist!")
