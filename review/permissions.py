from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Comment

class IsAuthorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return True


    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        if isinstance(obj, Comment):
            return request.user == obj.user_id
