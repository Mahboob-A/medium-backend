from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import APIException
from rest_framework.status import HTTP_400_BAD_REQUEST


class YouHaveAlreadyRatedException(APIException):
    status_code = HTTP_400_BAD_REQUEST
    default_detail = _("You have already rated this article")
    default_code = "bad_request"


class YouCanNotRateYourOwnArticleException(APIException):
    status_code = HTTP_400_BAD_REQUEST
    default_detail = _("You can not rate your own article")
    default_code = "bad_request"
