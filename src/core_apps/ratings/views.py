from django.shortcuts import render
from django.db import IntegrityError

from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError

from core_apps.ratings.exceptions import YouHaveAlreadyRatedException, YouCanNotRateYourOwnArticleException
from core_apps.articles.models import Article

from .models import Ratings
from .serializers import RatingSerializer



class RatingCreateView(generics.CreateAPIView): 
        ''' API to create Rating instances for Article Model '''
        queryset = Ratings.objects.all()
        serializer_class = RatingSerializer
        permission_classes = [permissions.IsAuthenticated]
        
        def perform_create(self, serializer):
                article_id = self.kwargs.get('article_id')
                
                if article_id: 
                        try: 
                                article = Article.objects.get(id=article_id)
                                if article.author == self.request.user: 
                                        raise YouCanNotRateYourOwnArticleException
                        except Article.DoesNotExist: 
                                raise ValidationError('The Article ID is invalid.')
                else: 
                        raise ValidationError('Article ID is required.')

                try: 
                        serializer.save(user=self.request.user, article=article)
                except IntegrityError: 
                        raise YouHaveAlreadyRatedException
