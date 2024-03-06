from django.shortcuts import render

# Create your views here.
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView

from django.contrib.auth import get_user_model

from .serializers import UserSerializer


class CustomUserDetailsView(RetrieveUpdateAPIView): 
        ''' API for authenticated user's details '''
        serializer_class = UserSerializer
        permission_classes = [IsAuthenticated, ]
        
        
        def get_object(self):
                return self.request.user 

        def get_queryset(self):
                return get_user_model().objects.none()


