
from rest_framework.pagination import PageNumberPagination


class ArticlePageNumberPagination(PageNumberPagination): 
        page_size = 10 
        page_query_param = 'page'
        max_page_size = 25 