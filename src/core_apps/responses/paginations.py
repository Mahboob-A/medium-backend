from rest_framework.pagination import PageNumberPagination


class ResponsesPageNumberPagination(PageNumberPagination):
    page_size = 1
    max_page_size = 25
    page_size_query_param = "limit"
