from rest_framework.permissions import BasePermission

class IsProductOwner(BasePermission):
    message = "You are not the owner of this product."
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
    