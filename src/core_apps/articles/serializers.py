from rest_framework import serializers
from .models import Article, ArticleViews
from core_apps.profiles.serializer import ProfileSerializer


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
        author_details = ProfileSerializer(source='author.profile', read_only=True)  # Article.author (author is ForeignKey with User.) => In Profile model, Profile has one-to-one with User with related name 'profile'
        estimated_reading_time = serializers.ReadOnlyField() # as estimated_reading_time is property, no need to have any method here 
        
        average_rating = serializers.ReadOnlyField()
        
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
                fields = ['id', 'author_details', 'title', 'slug', 'description', 'body', 'banner_image', 'body_image_1', 'body_image_2', 
                          'tags', 'estimated_reading_time', 'banner_image', 'views', 'created_at', 'updated_at', 
                ]
        
        
        
        
        
        
        
        
        