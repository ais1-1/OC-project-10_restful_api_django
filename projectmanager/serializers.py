from rest_framework import serializers

from .models import Project, Contributor, Issue, Comment
from authentication.serializers import UserListSerializer


class ProjectListSerializer(serializers.ModelSerializer):
    created_time = serializers.ReadOnlyField()

    class Meta(object):
        model = Project

        fields = ("id", "name", "created_time")


class ProjectDetailSerializer(serializers.ModelSerializer):
    created_time = serializers.ReadOnlyField()

    class Meta(object):
        model = Project

        fields = ("name", "description", "project_type", "author", "created_time")


class ContributorDetailSerializer(serializers.ModelSerializer):
    user = UserListSerializer()
    project = ProjectDetailSerializer(many=True)
    created_time = serializers.ReadOnlyField()

    class Meta(object):
        model = Contributor

        fields = ("id", "user", "project", "created_time")


class ContributorListSerializer(serializers.ModelSerializer):
    created_time = serializers.ReadOnlyField()

    class Meta(object):
        model = Contributor

        fields = ("id", "user", "project", "created_time")


class IssueListSerializer(serializers.ModelSerializer):
    created_time = serializers.ReadOnlyField()

    class Meta(object):
        model = Issue

        fields = (
            "id",
            "name",
            "priority",
            "assigned_to",
            "status",
            "project",
            "created_time",
        )


class IssueDetailSerializer(serializers.ModelSerializer):
    created_time = serializers.ReadOnlyField()
    author = ContributorDetailSerializer()
    assigned_to = ContributorDetailSerializer()
    project = ProjectDetailSerializer()

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
        )


class CommentDetailSerializer(serializers.ModelSerializer):
    created_time = serializers.ReadOnlyField()
    author = ContributorDetailSerializer()
    issue = IssueListSerializer()

    class Meta(object):
        model = Comment

        fields = ("id", "description", "author", "issue", "created_time")


class CommentListSerializer(serializers.ModelSerializer):
    created_time = serializers.ReadOnlyField()

    class Meta(object):
        model = Comment

        fields = ("id", "description", "author", "issue", "created_time")
