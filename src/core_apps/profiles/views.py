from django.shortcuts import render

# Create your views here.
# TODO change the .dev into production in Production 
from medium_backend.settings.dev import DEFAULT_FROM_EMAIL

# django
from django.core.mail import send_mail 
from django.contrib.auth import get_user_model

# drf 
from rest_framework.permissions import IsAuthenticated
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
from .serializer import ProfileUpdateSerializer, ProfileSerializer, FollowingSerializer


User = get_user_model()

class ProfileListAPIView(generics.ListAPIView): 
        queryset = Profile.objects.all()
        pagination_class = ProfilePagination
        serializer_class = ProfileSerializer
        renderer_classes = [ProfilesJSONRenderer]
        

class ProfileDetailAPIView(generics.RetrieveAPIView):
        permission_classes = [IsAuthenticated]
        serializer_class = ProfileSerializer
        renderer_classes = [ProfileJSONRenderer]
         
         
        def get_queryset(self):
                queryset = Profile.objects.select_related('user')
                return queryset

        def get_object(self):
                user = self.request.user 
                profile = self.get_queryset().get(user=user)
                return profile

                # as profile as one to one with user 
                # return self.request.user.profile
        


class ProfileUpdateAPIView(generics.UpdateAPIView): 
        serializer_class = ProfileUpdateSerializer
        



































