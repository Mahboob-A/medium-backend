
from django.urls import path 

from .views import ArticleListCreateView, ArticleRetriveUpdateDestroyView


urlpatterns = [
        path('', ArticleListCreateView.as_view(), name='article_list_create_api'), 
        path('<uuid:id>/', ArticleRetriveUpdateDestroyView.as_view(), name='article_retrive_update_destroy_api'), 
]
