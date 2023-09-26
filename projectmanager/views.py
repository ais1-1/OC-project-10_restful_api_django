from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

from .models import Project, Contributor, Issue, Comment
from .serializers import (
    ProjectDetailSerializer,
    ProjectListSerializer,
    IssueListSerializer,
    IssueDetailSerializer,
    CommentListSerializer,
    ContributorListSerializer,
)
from .permissions import (
    ProjectPermission,
    IssuePermission,
    CommentPermission,
    ContributorPermission,
    is_contributor,
)
from .mixins import GetDetailSerializerMixin

User = get_user_model()


class ProjectViewset(GetDetailSerializerMixin, ModelViewSet):
    """
    Project views endpoints.
    Create: Anyone
    Get list / details: Contributor
    Update / delete: Author
    """

    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer
    queryset = Project.objects.all()

    permission_classes = [IsAuthenticated, ProjectPermission]

    @transaction.atomic
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        project = super(ProjectViewset, self).create(request, *args, **kwargs)
        contributor = Contributor.objects.create(
            user=request.user,
            project=Project.objects.filter(id=project.data["id"]).first(),
        )
        contributor.save()
        return Response(project.data, status=status.HTTP_201_CREATED)


class ContributorViewset(ModelViewSet):
    """
    Contributor views endpoints.
    Create/ update /delete: Author of a project
    Get list / details: Contributor
    """

    serializer_class = ContributorListSerializer

    permission_classes = [IsAuthenticated, ContributorPermission]

    def get_queryset(self):
        """Verify the presence of ‘project_id’ in the url,
        if yes apply filter to show contributors of the given project"""
        project_id = self.request.GET.get("project_id")
        if project_id is not None and is_contributor(
            self.request.user, get_object_or_404(Project, id=project_id)
        ):
            queryset = Contributor.objects.filter(
                project=get_object_or_404(Project, id=project_id)
            )
            return queryset
        else:
            raise ValidationError(
                detail="Apply a filter with project_id; a project that you are contributing to."
            )

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        # if user exists create Contributor
        if User.objects.filter(id=request.data["user"]).exists():
            user = get_object_or_404(User, id=request.data["user"])
            # Create contributor if doesn't exist
            contributor, create = Contributor.objects.get_or_create(
                user=user,
                project=get_object_or_404(Project, id=request.data["project"]),
            )
            return Response(status=status.HTTP_201_CREATED)

        else:
            return Response(
                {"error": "User does not exists !"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        # if user exists get Contributor
        if User.objects.filter(id=request.data["user"]).exists():
            user = get_object_or_404(User, id=request.data["user"])
            if user == request.user:
                return Response(
                    {"error": "You cannot delete yourself !"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # Delete contributor if exist
            contributor = get_object_or_404(
                Contributor,
                user=user,
                project=get_object_or_404(Project, id=request.data["project"]),
            )
            contributor.delete()
            return Response(status=status.HTTP_201_CREATED)

        else:
            return Response(
                {"error": "User does not exists !"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class IssueViewset(GetDetailSerializerMixin, ModelViewSet):
    """
    Issue views endpoints.
    Create/ update /delete: Author Contributor
    Get list / details: Contributor
    """

    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer

    permission_classes = [IsAuthenticated, IssuePermission]

    def get_queryset(self):
        """Verify the presence of ‘project_id’ in the url,
        if yes and if the user is a contributor of this project
        apply filter to show issues of the given project"""
        project_id = self.request.GET.get("project_id")
        if project_id is not None and is_contributor(
            self.request.user, get_object_or_404(Project, id=project_id)
        ):
            queryset = Issue.objects.filter(
                project=get_object_or_404(Project, id=project_id)
            )
            return queryset
        else:
            raise ValidationError(
                detail="Apply a filter with project_id; a project that you are contributing to."
            )

    @transaction.atomic
    def perform_create(self, serializer):
        serializer.save(
            description=self.request.data["description"],
            author=get_object_or_404(
                Contributor,
                user=self.request.user,
                project=self.request.data["project"],
            ),
        )


class CommentViewset(GetDetailSerializerMixin, ModelViewSet):
    """
    Comment views endpoints.
    Create/ update /delete: Author Contributor
    Get list / details: Contributor
    """

    serializer_class = CommentListSerializer

    permission_classes = [IsAuthenticated, CommentPermission]

    def get_queryset(self):
        """Verify the presence of 'issue_id' in the url,
        if yes and if the user is a contributor of the project in which the issue is
        apply filter to show the comments of the given issue"""
        issue_id = self.request.GET.get("issue_id")
        if issue_id is not None and is_contributor(
            self.request.user, get_object_or_404(Issue, id=issue_id).project
        ):
            queryset = Comment.objects.filter(
                issue=get_object_or_404(Issue, id=issue_id)
            )
            return queryset
        else:
            raise ValidationError(
                detail="Apply a filter with issue_id; an issue which is part of a project that you are contributing to."
            )

    @transaction.atomic
    def perform_create(self, serializer):
        serializer.save(
            author=get_object_or_404(
                Contributor,
                user=self.request.user,
                project=get_object_or_404(Issue, id=self.request.data["issue"]).project,
            )
        )
