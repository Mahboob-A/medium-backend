from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView

# Create your views here.
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer

User = get_user_model()


class CustomUserDetailsView(RetrieveUpdateAPIView):
    """API for authenticated user's details"""

    serializer_class = UserSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        return get_user_model().objects.none()


class CustomUserDetailsView2(APIView):
    """API for authenticated user's details"""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = User.objects.get(id=self.request.user.id)
        serializer = UserSerializer(user)
        return Response(
            {"status": "success", "data": serializer.data}, status=status.HTTP_200_OK
        )
