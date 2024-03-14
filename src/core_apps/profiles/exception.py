from rest_framework.exceptions import APIException
from django.utils.translation import gettext_lazy as _ 
from rest_framework.status import HTTP_403_FORBIDDEN


class CanNotFollowYouself(APIException): 
        status_code = HTTP_403_FORBIDDEN
        default_code = 'forbidden'
        default_detail = _('You can not follow yourself!')

