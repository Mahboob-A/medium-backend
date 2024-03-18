from rest_framework.exceptions import APIException
from rest_framework.status import HTTP_400_BAD_REQUEST
from django.utils.translation import gettext_lazy as _


class YouHaveAlreadyBookmarkedException(APIException):
    status_code = HTTP_400_BAD_REQUEST
    default_detail = _("You have already bookmarked the article")
    default_code = "bad_request"
