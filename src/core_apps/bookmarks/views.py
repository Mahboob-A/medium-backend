from uuid import UUID, uuid4

from django.db import IntegrityError
from django.shortcuts import render
from rest_framework import generics
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core_apps.articles.models import Article

from .exceptions import YouHaveAlreadyBookmarkedException
from .models import Bookmark
from .paginations import BookmarkPageNumberPagination
from .renderers import BookmarkJSONRenderer, BookmarksJSONRenderer
from .serializers import BookmarkSerializer


class BookmarkCreateAPIView(generics.CreateAPIView):
    """API to add bookmark"""

    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        article_id = self.kwargs.get("article_id")

        if article_id:
            try:
                article = Article.objects.get(id=article_id)
            except Article.DoesNotExist:
                raise ValidationError("Article ID is not valid")
        else:
            raise ValidationError("Article ID is required")

        try:
            serializer.save(user=self.request.user, article=article)
        except IntegrityError:
            raise YouHaveAlreadyBookmarkedException


class BookmarkDestroyAPIView(generics.DestroyAPIView):
    """API to delete bookmark"""

    queryset = Bookmark.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = "article_id"

    def get_object(self):
        """get_object() -> to fetch singel object."""
        user = self.request.user
        article_id = self.kwargs.get("article_id")

        # Verify the uuid if it is correct uuid
        # try:
        #         UUID(str(article_id), version=4)
        # except ValueError:
        #         raise ValidationError('Invalid Article ID')

        try:
            bookmark = Bookmark.objects.get(user=user, article__id=article_id)
        except Bookmark.DoesNotExist:
            raise NotFound("Bookmark not found or it might be already deleted")

        return bookmark

    def perform_destroy(self, instance):
        if self.request.user != instance.user:
            raise ValidationError(
                "Bookmark can not be deleted as the bookmark is not yours."
            )

        instance.delete()


class AllBookmarksOfUserAPIView(generics.ListAPIView):
    """All bookmarks of an User"""

    serializer_class = BookmarkSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = BookmarkPageNumberPagination
    renderer_classes = [BookmarksJSONRenderer]

    def get_queryset(self):
        bookmarks = Bookmark.objects.filter(user=self.request.user)
        return bookmarks

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        total_bookmarks = queryset.count()
        page = self.paginate_queryset(queryset=queryset)

        if page is not None:
            serializer = self.get_serializer(queryset, many=True)
            response_data = {
                "total_bookmarks": total_bookmarks,
                "data": serializer.data,
            }
            return self.get_paginated_response(response_data)

        # if pagination has not been used.
        serializer = self.get_serializer(queryset, many=True)
        response_data = {"total_bookmarks": total_bookmarks, "data": serializer.data}
        return Response(response_data)
