from django.shortcuts import render
import logging

from django.http import Http404, HttpResponse
from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework import filters, generics, permissions, status

from django_filters.rest_framework import DjangoFilterBackend


from .models import Article, ArticleReadTimeEngine, ArticleViews
from .serializers import ArticleSerializer
from .pagination import ArticlePageNumberPagination
from .renderers import ArticleJSONRenderer, ArticlesJSONRenderer
from .permissions import IsOwnerOrReadOnly
from .filters import ArticleFilter


User = get_user_model()
logger = logging.getLogger(__name__)


class ArticleListCreateView(generics.ListCreateAPIView): 
        ''' Article API fot Listing and Creating Articles '''
        queryset = Article.objects.all()
        serializer_class = ArticleSerializer
        # TODO as ArticleFilters is having some issue, fix it later once the project is ready to run 
        filterset_class = ArticleFilter 
        pagination_class = ArticlePageNumberPagination
        
        permission_classes = [permissions.IsAuthenticated]
        renderer_classes = [ArticlesJSONRenderer]
        ordering_fields = ['-crearted_at', '-updated_at']
        filter_backends = [DjangoFilterBackend, filters.OrderingFilter]

        def perform_create(self, serializer):
                serializer.save(author=self.request.user)
                
                logger.info(
                        f'Article {serializer.data.get("title")} created by {self.request.user.first_name.title()} {self.request.user.last_name.title()}'
                )
                
                
                
                
                
class ArticleRetriveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView): 
        queryset = Article.objects.all()
        serializer_class = ArticleSerializer
        permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]        
        renderer_classes = [ArticlesJSONRenderer]
        lookup_field = 'id'  # to retrive object similart to passing the id to method's param in function based view 

        def perform_update(self, serializer):
                serializer.save(author=self.request.user)
        
        # update the view count as an Article is being retrived/viewed 
        def retrieve(self, request, *args, **kwargs):
                try: 
                        instance = self.get_object()
                except Http404: 
                        return Response({'message' : 'Article does not found'}, status=status.HTTP_404_NOT_FOUND)

                # get the serializer class used in the API 
                serializer = self.get_serializer(instance)
                
                viewer_ip = request.META.get('REMOTE_ADDR', None)
                
                # add article view in ArticleViews model 
                ArticleViews.record_view(article=instance, user=request.user, viewer_ip=viewer_ip)
                
                return Response(serializer.data, status=status.HTTP_200_OK)