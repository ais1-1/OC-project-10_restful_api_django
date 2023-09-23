from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Project, Contributor, Issue, Comment
from .serializers import (
    ProjectDetailSerializer,
    ProjectListSerializer,
    ContributorListSerializer,
    ContributorDetailSerializer,
    IssueListSerializer,
    IssueDetailSerializer,
    CommentDetailSerializer,
    CommentListSerializer,
)
from .permissions import ProjectPermission, IssuePermission, CommentPermission


class MultipleSerializerMixin:
    """Mixin for accessing detailed serializer if the action is retrieve"""

    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == "retrieve" and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


class ProjectViewset(MultipleSerializerMixin, ModelViewSet):
    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer
    queryset = Project.objects.all()

    permission_classes = [IsAuthenticated, ProjectPermission]


class ContributorViewset(MultipleSerializerMixin, ModelViewSet):
    serializer_class = ContributorListSerializer
    detail_serializer_class = ContributorDetailSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Show the list of the projects where the contributor is part of"""
        queryset = Contributor.objects.filter(user=self.request.user)
        return queryset


class IssueViewset(MultipleSerializerMixin, ModelViewSet):
    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer

    permission_classes = [IsAuthenticated, IssuePermission]

    def get_queryset(self):
        queryset = Issue.objects.all()
        """ Verify the presence of ‘project_id’ in the url,
        if yes apply filter to show issues of the given project """
        project_id = self.request.GET.get("project_id")
        if project_id is not None:
            queryset = queryset.filter(
                project=get_object_or_404(Project, id=project_id)
            )
        return queryset


class CommentViewset(MultipleSerializerMixin, ModelViewSet):
    serializer_class = CommentListSerializer
    detail_serializer_class = CommentDetailSerializer

    permission_classes = [IsAuthenticated, CommentPermission]

    def get_queryset(self):
        queryset = Comment.objects.all()
        """ Verify the presence of 'issue_id' in the url,
        if yes apply filter to show the comments of the given issue """
        issue_id = self.request.GET.get("issue_id")
        if issue_id is not None:
            queryset = queryset.filter(issue=get_object_or_404(Issue, id=issue_id))
        return queryset
