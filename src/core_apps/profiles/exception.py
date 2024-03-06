from rest_framework.exceptions import APIException


class CanNotFollowYouself(APIException): 
        status_code = 403 
        default_code = 'forbidden'
        default_detail = 'You can not follow yourself!'

