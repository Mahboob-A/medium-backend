from django.shortcuts import render, get_object_or_404
import logging

from django.http import Http404, HttpResponse
from django.core.files.storage import default_storage
from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework import filters, generics, permissions, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.exceptions import ValidationError

from django_filters.rest_framework import DjangoFilterBackend


from .models import Article, ArticleReadTimeEngine, ArticleViews, Clap
from .serializers import ArticleSerializer, ArticleSerializerForAllArticleListView, ClapSerializer
from .pagination import ArticlePageNumberPagination
from .renderers import ArticleJSONRenderer, ArticlesJSONRenderer
from .permissions import IsOwnerOrReadOnly
from .exceptions import AuthorNotFoundException, AlreadyClappedOnThisArticle
from .filters import ArticleFilter

from core_apps.profiles.serializer import ProfileSerializer
from core_apps.responses.serializers import ResponseSerializer
from core_apps.responses.paginations import ResponsesPageNumberPagination

User = get_user_model()
logger = logging.getLogger(__name__)


class ArticleListCreateView(generics.ListCreateAPIView): 
        ''' Article API fot Listing and Creating Articles '''
        queryset = Article.objects.all()
        serializer_class = ArticleSerializerForAllArticleListView
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
        
        def update(self, request, *args, **kwargs):
                # instance = serializer.save(author=self.request.user)
                partial = kwargs.pop('partial', False)
                instance = self.get_object()
                serializer = self.get_serializer(instance, data=request.data, partial=partial)
                serializer.is_valid(raise_exception=True)
 
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
                
                # add the authors details in the response 
                profile = self.request.user.profile 
                profile_serializer_data = ProfileSerializer(profile).data 
        
                
                data = {}
                data['authors_datails'] = profile_serializer_data
                data['data'] =  serializer.data

                # the Response is filtered in according to the renderer_classes defined in the API class. 
                # the structure of data that is passed is defined in the renderer_classes in defined in the API class. 
                return Response(data, status=status.HTTP_200_OK)
                
                
                
        # update the view count as an Article is being retrived/viewed 
        def retrieve(self, request, *args, **kwargs):
                try: 
                        instance = self.get_object()
                except Http404: 
                        return Response({'message' : 'Article does not found'}, status=status.HTTP_404_NOT_FOUND)

                
                
                viewer_ip = request.META.get('REMOTE_ADDR', None)
                
                # add article view in ArticleViews model 
                ArticleViews.record_view(article=instance, user=request.user, viewer_ip=viewer_ip)
                
                # add the authors details in the response 
                profile = self.request.user.profile 
                profile_serializer_data = ProfileSerializer(profile).data 
                
                # get the serializer class of Article used in the class 
                article_serializer_data = self.get_serializer(instance).data
                
                data = {}
                data['authors_datails'] = profile_serializer_data
                data['data'] =  article_serializer_data

                # the Response is filtered in according to the renderer_classes defined in the API class. 
                # the structure of data that is passed is defined in the renderer_classes in defined in the API class. 
                return Response(data, status=status.HTTP_200_OK)
        



class AllArticleOfAuthor(generics.ListAPIView): 
        ''' API for all articles of an Author'''
        serializer_class = ArticleSerializer
        pagination_class = ArticlePageNumberPagination
        renderer_classes = [ArticlesJSONRenderer]
        permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        filterset_class = ArticleFilter
        ordering_fields = ['-crearted_at', '-updated_at']
        filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
        
        def get_queryset(self):
                author_id = self.kwargs.get('author_id')
                
                if author_id: 
                        try: 
                                author = User.objects.get(id=author_id)
                                self.queryset = author.articles.all()
                                return self.queryset
                                # self.queryset = Article.objects.filter(author=author)
                                # return self.queryset
                        except User.DoesNotExist: 
                                raise AuthorNotFoundException(detail='Author ID is incorrect')
                else: 
                        raise ValidationError('Author ID is required')
        
        def list(self, request, *args, **kwargs):
                queryset = self.get_queryset()
                total_articles = queryset.count()
                page = self.paginate_queryset(queryset=queryset)
                
                if page is not None: 
                        article_serializer = self.get_serializer(queryset, many=True)
                        profile_serializer = ProfileSerializer(self.request.user.profile)
                        response_data = {
                                'author_details' : profile_serializer.data,
                                'total_articles' : total_articles, 
                                'data' : article_serializer.data, 
                                
                        }
                        return self.get_paginated_response(response_data)
                
                
                # if pagination has not been used. 
                article_serializer = self.get_serializer(queryset, many=True)
                profile_serializer = ProfileSerializer(self.request.user.profile)
                response_data = {
                        'author_details' : profile_serializer.data,
                        'total_articles' : total_articles, 
                        'data' : article_serializer.data, 
                }        
                return Response(response_data)



class ClapCreateDestroyView(generics.CreateAPIView, generics.DestroyAPIView): 
        queryset = Clap.objects.all()
        serializer_class = ClapSerializer 

        def create(self, request, *args, **kwargs): 
                user = request.user 
                article_id = kwargs.get('article_id')
                article = get_object_or_404(Article, id=article_id)
                
                if Clap.objects.filter(user=user, article=article).exists(): 
                        # return Response({'detail' : 'You have already clapped on this article'}, status=status.HTTP_400_BAD_REQUEST)
                        raise AlreadyClappedOnThisArticle
                
                clap = Clap.objects.create(user=user, article=article)
                clap.save()
                return Response({'detail' : 'Clap is added to article'}, status=status.HTTP_201_CREATED)
        


        def destroy(self, request, *args, **kwargs): # def delete(self, request, *args, **kwargs)
                user = request.user 
                article_id = kwargs.get('article_id')
                article = get_object_or_404(Article, id=article_id)
                clap = get_object_or_404(Clap, user=user, article=article)
                clap.delete()
                return Response({'detail' : 'Clap is removed from article'}, status=status.HTTP_204_NO_CONTENT)










