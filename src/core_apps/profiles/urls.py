from django.urls import path

from .views import (
    FollowAUserAPIView,
    ProfileDetailAPIView,
    ProfileListAPIView,
    ProfileUpdateAPIView,
    UnfollowAUserAPIView,
    UserFollowerAPIView,
    UserFollowingAPIView,
)

urlpatterns = [
    # List View and Update view
    path("all-user-profiles/", ProfileListAPIView.as_view(), name="all-user-profiles"),
    path("me/", ProfileDetailAPIView.as_view(), name="my-profile"),
    path("me/update/", ProfileUpdateAPIView.as_view(), name="update-my-profile"),
    # see followrs and following of a user
    path("me/followers/", UserFollowerAPIView.as_view(), name="my-followers"),
    path("me/following/", UserFollowingAPIView.as_view(), name="me-following"),
    # follow and unfollow
    path(
        "me/follow/<uuid:user_id>/", FollowAUserAPIView.as_view(), name="follow-a-user"
    ),
    path(
        "me/unfollow/<uuid:user_id>/",
        UnfollowAUserAPIView.as_view(),
        name="unfollow-a-user",
    ),
]
