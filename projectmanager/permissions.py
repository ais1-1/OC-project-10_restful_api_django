from rest_framework.permissions import BasePermission, SAFE_METHODS

from .models import Contributor


def is_contributor(user, project):
    for contributor in Contributor.objects.filter(project=project):
        if user is contributor.user:
            return True
    return False


class ProjectPermission(BasePermission):
    """Only contributors have access. And only an author can update, partial update, destroy actions.
    Instance must have an attribute named `author`."""

    message = "Only contributors have permission."

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return is_contributor(request.user, obj)
        else:
            return obj.author == request.user


class IssuePermission(BasePermission):
    """Only contributors have access. And only an author can update, partial update, destroy actions.
    Instance must have an attribute named `author`."""

    message = "Only contributors have permission."

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return is_contributor(request.user, obj.project)
        else:
            return obj.author == request.user


class CommentPermission(BasePermission):
    """Only contributors have access. And only an author can update, partial update, destroy actions.
    Instance must have an attribute named `author`."""

    message = "Only contributors have permission."

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return is_contributor(request.user, obj.issue.project)
        else:
            return obj.author == request.user
