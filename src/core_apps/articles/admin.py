from django.contrib import admin

# Register your models here.
from .models import Article, ArticleViews, Clap


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin): 
        list_display = ['pkid', 'id', 'author', 'title', 'get_view_count', 'tags']
        list_display_links = ['pkid', 'id', 'author', 'title']
        list_filter =  ['created_at', 'updated_at']
        search_fields = ['title', 'author__first_name', 'tags__name']  # for searcing, do not directly use foreignkey field, use  __fieldname convention to locate proper field from foreignkey
        ordering = ['-created_at']
        
        readonly_fields = ['view_count']
        date_hierarchy = 'created_at'
        fieldsets = [
                ('Article Information', {'fields': ['title', 'author']}),
                ('Content', {'fields': ['description', 'body', 'tags']}),
                ('Media', {'fields' : ['banner_image', 'body_image_1', 'body_image_2']}), 
                ('Analytics', {'fields': ['view_count']}),
        ]
        
        def get_view_count(self, obj): 
                return obj.view_count()
        
@admin.register(ArticleViews)
class ArticleViewAdmin(admin.ModelAdmin): 
        list_display = ['id', 'article', 'user', 'viewer_ip']
        list_display_links = [ 'id', 'article', 'user']
        list_filter =  ['created_at', 'updated_at']
        search_fields = ['article', 'user', 'viewer_ip']
        ordering = ['-created_at']


@admin.register(Clap)
class ClapAdmin(admin.ModelAdmin): 
        list_display = ['id', 'article', 'user', ]
        list_display_links = ['id', 'article', 'user']
        list_filter =  ['created_at', 'updated_at']
        