from django.shortcuts import render
import logging

from django.http import Http404, HttpResponse
from django.core.files.storage import default_storage
from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework import filters, generics, permissions, status
from rest_framework.parsers import MultiPartParser, FormParser

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
        renderer_classes = [ArticleJSONRenderer]
        lookup_field = 'id'  # to retrive object similart to passing the id to method's param in function based view 
        parser_classes = [MultiPartParser, FormParser]  # to handle file/image upload 
        
        def perform_update(self, serializer):
                instance = serializer.save(author=self.request.user)
                
                # TODO the old images are not being deleted after the patch or put update. Fix the issue. 
                # Debug prints  
                # print(f"Old banner_image path: {instance.banner_image.path if instance.banner_image else 'None'}")
                # print(f"Old body_image_1 path: {instance.body_image_1.path if instance.body_image_1 else 'None'}")
                # print(f"Old body_image_2 path: {instance.body_image_2.path if instance.body_image_2 else 'None'}")
                
                # check if any images are passed to update - then delete the old image and update the new image 
                if 'banner_image' in self.request.FILES: 
                        # only delete any old image by the user, do not delete the default image
                        if instance.banner_image and instance.banner_image.name != 'article-default.png':
                                default_storage.delete(instance.banner_image.path)
                        
                        # set the new image 
                        instance.banner_image = self.request.FILES.get('banner_image')
                        
                        
                # update if body_image_1
                if 'body_image_1' in self.request.FILES: 
                        if instance.body_image_1 and instance.body_image_1.name != 'article-default.png':
                                default_storage.delete(instance.body_image_1.path)
                                
                        instance.body_image_1 = self.request.FILES.get('body_image_1')
                        
                
                # update  if body_image_2
                if 'body_image_2' in self.request.FILES: 
                        if instance.body_image_2 and instance.body_image_2.name != 'article-default.png':
                                default_storage.delete(instance.body_image_2.path)
                                
                        instance.body_image_2 = self.request.FILES.get('body_image_2')
                        
                
                # save the changes 
                instance.save()
                # print(f"New banner_image path: {instance.banner_image.path if instance.banner_image else 'None'}")
                # print(f"new body_image_1 path: {instance.body_image_1.path if instance.body_image_1 else 'None'}")
                # print(f"New body_image_2 path: {instance.body_image_2.path if instance.body_image_2 else 'None'}")
                
                
                
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