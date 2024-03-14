
from django_filters import filters, FilterSet

from .models import Article

class ArticleFilter(FilterSet): 
        ''' Filter for core_apps.article.Article model '''
        author = filters.CharFilter(field_name='author__first_name', lookup_expr='icontains')
        title = filters.CharFilter(field_name='title', lookup_expr='icontains')
        tags = filters.CharFilter(field_name='tags__name', lookup_expr='icontains') # for filtering, do not directly use foreignkey field, use  __fieldname convention to locate proper field from foreignkey
        created_at = filters.DateFromToRangeFilter(field_name='created_at')
        updated_at = filters.DateTimeFromToRangeFilter(field_name='updated_at')
        
        class Meta: 
                model = Article
                fields = ['author', 'title', 'tags', 'created_at', 'updated_at']