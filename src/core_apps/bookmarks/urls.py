from django.urls import path

from .views import BookmarkCreateAPIView, BookmarkDestroyAPIView



urlpatterns = [
        path('bookmark/add/<uuid:article_id>/', BookmarkCreateAPIView.as_view(), name='bookmark_add'), 
        path('bookmark/remove/<uuid:article_id>/', BookmarkDestroyAPIView.as_view(), name='bookmark_remove')
]
