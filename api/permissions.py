from rest_framework.generics import get_object_or_404
from rest_framework.permissions import BasePermission, SAFE_METHODS

from .models import Contributor, Issue


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


class IsProjectAuthorOrContributorReadAndPost(BasePermission):
    """ Contributors can Read everything and Post
    and the project author has all permissions."""

    def has_permission(self, request, view):
        project_id = view.kwargs.get("project_pk")
        contributors = [
            contrib.user for contrib in Contributor.objects.filter(project=project_id)
        ]
        return bool(request.user in contributors)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return bool(obj.project.author_user == request.user)


class IsIssueAuthorOrContributorReadAndPost(BasePermission):
    """ Contributors can Read everything and Post
        and the issue author has all permissions."""

    def has_permission(self, request, view):
        project_id = view.kwargs.get("project_pk")
        contributors = [
            contrib.user for contrib in Contributor.objects.filter(project=project_id)
        ]
        return bool(request.user in contributors)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return bool(obj.author_user == request.user)


class IsCommentAuthorOrContributorReadAndPost(BasePermission):
    """ Contributors can Read everything and Post
        and the comment author has all permissions."""

    def has_permission(self, request, view):
        project_id = view.kwargs.get("project_pk")
        contributors = [
            contrib.user for contrib in Contributor.objects.filter(project=project_id)
        ]
        return bool(request.user in contributors)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return bool(obj.author_user == request.user)
