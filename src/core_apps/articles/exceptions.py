from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import APIException
from rest_framework.status import HTTP_400_BAD_REQUEST


class AuthorNotFoundException(APIException):
    status_code = HTTP_400_BAD_REQUEST
    default_detail = _("Author not found")
    default_code = "bad_request"


class AlreadyClappedOnThisArticle(APIException):
    status_code = HTTP_400_BAD_REQUEST
    default_detail = _("You have already clapped on this article")
    default_code = "bad_request"
