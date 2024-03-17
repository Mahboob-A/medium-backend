
from django.urls import path 


from .views import ResponseListCreateView, ResponseRetriveUpdateDeleteView

urlpatterns = [
        path('article/<uuid:article_id>/', ResponseListCreateView.as_view(), name='article_response_list_create_api'), 
        path('article/response/<uuid:contextid>/', ResponseRetriveUpdateDeleteView.as_view(), name='article_response_ret_update_del_api'),
]



