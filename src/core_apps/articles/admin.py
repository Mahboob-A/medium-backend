from django.contrib import admin

# Register your models here.
from .models import Article, ArticleViews


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin): 
        list_display = ['pkid', 'id', 'author', 'title', 'get_view_count', 'tags']
        list_display_links = ['pkid', 'id', 'author', 'title']
        list_filter =  ['created_at', 'updated_at']
        search_fields = ['title', 'author', 'tags']
        ordering = ['-created_at']
        
        readonly_fields = ['view_count']
        date_hierarchy = 'created_at'
        fieldsets = [
                ('Article Information', {'fields': ['title', 'author']}),
                ('Content', {'fields': ['description', 'body', 'tags']}),
                ('Analytics', {'fields': ['view_count']}),
        ]
        
        def get_view_count(self, obj): 
                return obj.view_count()
        
@admin.register(ArticleViews)
class ArticleAdmin(admin.ModelAdmin): 
        list_display = ['pkid', 'id', 'article', 'user', 'viewer_ip']
        list_display_links = ['pkid', 'id', 'article', 'user']
        list_filter =  ['created_at', 'updated_at']
        search_fields = ['article', 'user', 'viewer_ip']
        ordering = ['-created_at']