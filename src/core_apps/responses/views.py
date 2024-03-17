from django.shortcuts import render, get_object_or_404

from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from core_apps.articles.models import Article

from .models import Response
from .serializers import ResponseSerializer




class ResponseListCreateView(generics.ListCreateAPIView): 
        ''' API to list/create Responses/Comments by User to an Article '''
        queryset = Response.objects.all()
        serializer_class = ResponseSerializer
        permission_classes = [IsAuthenticated]
        
        def get_queryset(self):
                article_id = self.kwargs.get('article_id')
                return Response.objects.filter(article__id=article_id, parent_response=None)
        
        def perform_create(self, serializer):
                user = self.request.user 
                article_id = self.kwargs.get('article_id')
                article = get_object_or_404(Article, id=article_id)
                serializer.save(user=user, article=article)
                



class ResponseRetriveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView): 
        queryset = Response.objects.all()
        serializer_class = ResponseSerializer
        lookup_field = 'id'
        
        def perform_update(self, serializer):
                # self.get_object gets the object with get_object_or_404
                instance = self.get_object()
                
                if self.request.user  != instance.user: 
                        raise PermissionDenied('You do not have permission to edit the response.')
                
                serializer.save()
                
        
        def perform_destroy(self, instance):
                instance = self.get_object()
                
                if self.request.user  != instance.user: 
                        raise PermissionDenied('You do not have permission to delete the response.')
                
                instance.delete()