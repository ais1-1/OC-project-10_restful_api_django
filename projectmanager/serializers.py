from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Project, Contributor, Issue, Comment
from authentication.serializers import UserListSerializer

User = get_user_model()


class ProjectListSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Project

        fields = ("id", "name", "project_type", "author")


class ProjectDetailSerializer(serializers.ModelSerializer):
    created_time = serializers.ReadOnlyField()
    issues = serializers.SerializerMethodField()

    class Meta(object):
        model = Project

        fields = (
            "name",
            "description",
            "project_type",
            "author",
            "created_time",
            "issues",
        )

    def get_issues(self, instance):
        queryset = Issue.objects.filter(project_id=instance.id)
        return IssueListSerializer(queryset, many=True).data


class ContributorListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta(object):
        model = Contributor

        fields = ("id", "user", "project")

    def get_user(self, instance):
        queryset = User.objects.filter(id=instance.user.id)
        return UserListSerializer(queryset, many=True).data


class IssueListSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Issue

        fields = (
            "id",
            "name",
            "priority",
            "ticket",
            "assigned_to",
            "status",
            "project",
        )


class IssueDetailSerializer(serializers.ModelSerializer):
    created_time = serializers.ReadOnlyField()
    comments = serializers.SerializerMethodField()

    class Meta(object):
        model = Issue

        fields = (
            "id",
            "name",
            "description",
            "author",
            "assigned_to",
            "priority",
            "ticket",
            "status",
            "project",
            "created_time",
            "comments",
        )

    def get_comments(self, instance):
        queryset = Comment.objects.filter(issue_id=instance.id)
        return CommentListSerializer(queryset, many=True).data


class CommentListSerializer(serializers.ModelSerializer):
    created_time = serializers.ReadOnlyField()

    class Meta(object):
        model = Comment

        fields = ("id", "description", "author", "issue", "created_time")
