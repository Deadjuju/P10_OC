from rest_framework.permissions import BasePermission, SAFE_METHODS

from .models import Contributor


class IsProjectAuthorOrContributorDetailsOrReadOnly(BasePermission):
    """ The user must be authenticated to read,
    contributors have access to details
    and the project author has all permissions. """

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
    """ Permissions for contributors """

    def has_permission(self, request, view):
        project_id = view.kwargs.get("project_pk")
        contributors = [
            contrib.user for contrib in Contributor.objects.filter(project=project_id)
        ]
        return bool(request.user in contributors)


class IsProjectAuthorOrReadOnly(BasePermission):
    """ Permissions for project's author """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return bool(obj.project.author_user == request.user)


class IsIssueAuthorOrReadOnly(BasePermission):
    """ Permissions for issue's author """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return bool(obj.author_user == request.user)


class IsCommentAuthorOrReadOnly(BasePermission):
    """ Permissions for comment's author """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return bool(obj.author_user == request.user)
