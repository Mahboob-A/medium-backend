
from django.urls import path 


from .views import RatingCreateView


urlpatterns = [
        path('rate-article/<uuid:article_id>/', RatingCreateView.as_view(), name='create_rating'),
 
]
