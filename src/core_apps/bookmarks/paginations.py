
from rest_framework.pagination import PageNumberPagination

class BookmarkPageNumberPagination(PageNumberPagination): 
        page_size = 10 
        page_size_query_param = 'limit'
        max_page_size = 25
        page_query_param = 'page'