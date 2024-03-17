from django.contrib import admin

from .models import Response

@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin): 
        list_display = ['id', 'user', 'article', 'parent_response', 'context', 'created_at']
        list_display_links = ['id', 'user', 'article']
        

