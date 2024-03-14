from django.shortcuts import render
from django.db import IntegrityError

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError, NotFound

from uuid import UUID, uuid4

from core_apps.articles.models import Article

from .models import Bookmark
from .serializers import BookmarkSerializer
from .exceptions import YouHaveAlreadyBookmarkedException


class BookmarkCreateAPIView(generics.CreateAPIView): 
        ''' API to add bookmark '''
        queryset = Bookmark.objects.all()
        serializer_class = BookmarkSerializer
        permission_classes = [IsAuthenticated]
        
        def perform_create(self, serializer):
                article_id = self.kwargs.get('article_id')
                
                if article_id: 
                        try: 
                                article = Article.objects.get(id=article_id)
                        except Article.DoesNotExist: 
                                raise ValidationError('Article ID is not valid')
                else: 
                        raise ValidationError('Article ID is required')
        
                try: 
                        serializer.save(user=self.request.user, article=article)
                except IntegrityError: 
                        raise YouHaveAlreadyBookmarkedException
                
                
class BookmarkDestroyAPIView(generics.DestroyAPIView): 
        ''' API to delete bookmark '''
        queryset = Bookmark.objects.all()
        permission_classes = [IsAuthenticated]
        lookup_field = 'article_id'
        
        def get_object(self): 
                ''' get_object() -> to fetch singel object. '''
                user = self.request.user
                article_id = self.kwargs.get('article_id')
                
                # Verify the uuid if it is correct uuid 
                # try: 
                #         UUID(article_id, version=4)
                # except ValueError: 
                #         raise ValidationError('Invalid Article ID')
                
                try: 
                        bookmark = Bookmark.objects.get(user=user, article__id=article_id)
                except Bookmark.DoesNotExist: 
                        raise NotFound('Bookmark not found or it might be already deleted')
                
                return bookmark
                
        
        def perform_destroy(self, instance):
                if self.request.user != instance.user: 
                        raise ValidationError('Bookmark can not be deleted as the bookmark is not yours.')

                instance.delete()
        
        
        
        