from rest_framework import serializers
from .models import Article, ArticleViews, Clap
from core_apps.profiles.serializer import ProfileSerializer

from core_apps.bookmarks.models import Bookmark
from core_apps.bookmarks.serializers import BookmarkSerializer


class TagListField(serializers.Field): 
        ''' To get all the tags in a list/in list form '''
        def to_representation(self, value):
                return [tag.name for tag in value.all()]

        def to_internal_value(self, data):
                if not isinstance(data, list):
                        raise serializers.ValidationError('Expected a list of tags')
                
                all_tags = []
                for tag in data: 
                        tag = tag.strip()
                        # if the tag is now empty string after removing any trailing spaces, continue 
                        if not tag:
                                continue
                        all_tags.append(tag)
                return all_tags



class ArticleSerializer(serializers.ModelSerializer): 
        ''' Serializer class to serialize Article Object with other relevant details. Also passes Author Details while Serialize. '''
        # addint "author_details" here results in each article in a article queryset. hense, adding this from view only 
        # author_details = ProfileSerializer(source='author.profile', read_only=True)  # Article.author (author is ForeignKey with User.) => In Profile model, Profile has one-to-one with User with related name 'profile'
        estimated_reading_time = serializers.ReadOnlyField() # as estimated_reading_time is property, no need to have any method here 
        
        average_rating = serializers.ReadOnlyField()  # average_rating is not declared as @property hense a method is declared 
        
        banner_image = serializers.SerializerMethodField()
        views = serializers.SerializerMethodField()
        created_at = serializers.SerializerMethodField()
        updated_at = serializers.SerializerMethodField()
        
        # all bookmarks of user and its count 
        # the below fields also adds all the bookmarks made by all the users to this article. 
        # if we need to know how many users have bookmarked this article, then add the below two fields. 
        '''
        bookmarks = serializers.SerializerMethodField()
        total_bookmarks_count = serializers.SerializerMethodField()
        '''

        tags = TagListField()
        
        def get_banner_image(self, obj): 
                return obj.banner_image.url 
        
        # ArticleView model has ForeignKey relation with Article Model 
        def get_views(self, obj): 
                return ArticleViews.objects.filter(article=obj).count()

        def get_average_rating(self, obj): 
                return obj.average_rating()

        # get bookmarks 
        '''
        def get_bookmarks(self, obj): 
                bookmarks = Bookmark.objects.filter(article=obj)
                bookmark_serializer = BookmarkSerializer(bookmarks, many=True)
                return bookmark_serializer.data 
        
        # get bookmarks count 
        def get_total_bookmarks_count(self, obj): 
                return Bookmark.objects.filter(article=obj).count()
        '''
        
        def get_created_at(self, obj): 
                original_creation_date = obj.created_at 
                formatted_date = original_creation_date.strftime('%d/%m/%Y, %H:%M:%S')
                return formatted_date
        
        def get_updated_at(self, obj): 
                updated_date = obj.updated_at 
                formatted_date = updated_date.strftime('%d/%m/%Y, %H:%M:%S')
                return formatted_date
        
        def create(self, validated_data): 
                tags = validated_data.pop('tags')
                article = Article.objects.create(**validated_data)
                article.tags.set(tags)
                return article 
                
        
        def update(self, instance, validated_data): 
                instance.author = validated_data.get('author', instance.author)
                instance.title = validated_data.get('title', instance.title)
                instance.slug = validated_data.get('slug', instance.slug)
                instance.body = validated_data.get('body', instance.body)
                instance.description = validated_data.get('description', instance.description)
                instance.banner_image = validated_data.get('banner_image', instance.banner_image)
                instance.body_image_1 = validated_data.get('body_image_1', instance.body_image_1)
                instance.body_image_2 = validated_data.get('body_image_2', instance.body_image_2)
                instance.updated_at = validated_data.get('updated_at', instance.updated_at)
                
                if 'tags' in validated_data: 
                        instance.tags.set(validated_data.get('tags'))
                
                instance.save()
                return instance
        
        
        class Meta: 
                model = Article
                fields = ['id', 'title', 'slug', 'description', 'body', 'banner_image', 'body_image_1', 'body_image_2', 
                          'tags', 'estimated_reading_time', 'average_rating',  'banner_image', 'views', 
                          'created_at', 'updated_at', 
                ]
        
        
        
        
        
        
        
        
class ArticleSerializerForAllArticleListView(serializers.ModelSerializer): 
        ''' Serializer class to serialize Article Object for ListView of articles. '''
         
        author_details = ProfileSerializer(source='author.profile', read_only=True)  # Article.author (author is ForeignKey with User.) => In Profile model, Profile has one-to-one with User with related name 'profile'
        estimated_reading_time = serializers.ReadOnlyField() # as estimated_reading_time is property, no need to have any method here 
        
        average_rating = serializers.ReadOnlyField()  # average_rating is not declared as @property hense a method is declared 
        
        banner_image = serializers.SerializerMethodField()
        views = serializers.SerializerMethodField()
        created_at = serializers.SerializerMethodField()
        updated_at = serializers.SerializerMethodField()
        

        tags = TagListField()
        
        def get_banner_image(self, obj): 
                return obj.banner_image.url 
        
        # ArticleView model has ForeignKey relation with Article Model 
        def get_views(self, obj): 
                return ArticleViews.objects.filter(article=obj).count()

        def get_average_rating(self, obj): 
                return obj.average_rating()

        
        def get_created_at(self, obj): 
                original_creation_date = obj.created_at 
                formatted_date = original_creation_date.strftime('%d/%m/%Y, %H:%M:%S')
                return formatted_date
        
        def get_updated_at(self, obj): 
                updated_date = obj.updated_at 
                formatted_date = updated_date.strftime('%d/%m/%Y, %H:%M:%S')
                return formatted_date

        
        
        class Meta: 
                model = Article
                fields = ['author_details', 'id', 'title', 'slug', 'description', 'body', 'banner_image', 'body_image_1', 'body_image_2', 
                          'tags', 'estimated_reading_time', 'average_rating',  'banner_image', 'views', 
                          'created_at', 'updated_at', 
                ]
        

class ClapSerializer(serializers.ModelSerializer): 
        ''' Serializer for Clap model  '''
        article_title = serializers.CharField(source='article.title', read_only=True)
        user_first_name = serializers.CharField(source='user.first_name', read_only=True)
        user_last_name = serializers.CharField(source='user.last_name', read_only=True)
        
        class Meta: 
                model = Clap
                ields = ['id',  'article_title', 'user_first_name', 'user_last_name', 'created_at']
                read_only_fields = ['user']