from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwnerOrReadOnly(BasePermission):
    """Permission Class to Allow Un-safe Methods in Article objects Only to the Respective Author/User"""

    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS ('GET', 'HEAD', 'OPTIONS')
        if request.method in SAFE_METHODS:
            return True

        # if request not in SAFE_METHODS only grant if the object(article) is associated with author/user (as Article has relation with User with author key)
        # and request.user is also author/same user
        return bool(obj.author == request.user)
