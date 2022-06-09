from rest_framework.permissions import BasePermission, SAFE_METHODS

from .models import Contributor


class IsProjectAuthorOrContribOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        project_id = view.kwargs.get("pk")

        if view.action == "retrieve":
            contributors = [
                contrib.user for contrib in Contributor.objects.filter(project=project_id)
            ]
            return bool(request.user in contributors)

        if request.method in SAFE_METHODS:
            return True
        return obj.author_user == request.user


class IsContributor(BasePermission):
    pass
