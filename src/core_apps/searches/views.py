from django.shortcuts import render

from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    IdsFilterBackend,
    OrderingFilterBackend,
    DefaultOrderingFilterBackend,
    SearchFilterBackend,
)

from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet

from rest_framework.permissions import AllowAny

from .documents import ArticleDocument
from .serializers import ArticleElasticSearchSerializer


class ArticleElasticSearchView(DocumentViewSet):
    """API for enabling searching with Elasticsearch of Article Model"""

    document = ArticleDocument
    serializer_class = ArticleElasticSearchSerializer
    lookup_field = "id"  # for database lookup
    permission_classes = [AllowAny]

    filter_backends = [
        FilteringFilterBackend,
        IdsFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        SearchFilterBackend,
    ]

    # search by below fields
    search_fields = (
        "title",
        "description",
        "body",
        "author_first_name",
        "author_last_name",
        "tags",
    )

    filter_fields = {"slug": "slug.raw", "tags": "tags", "created_at": "created_at"}

    ordering_fields = {"created_at": "created_at"}

    ordering = "-created_at"
