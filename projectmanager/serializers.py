from rest_framework import serializers

from .models import Project, Contributor, Issue, Comment
from authentication.serializers import UserSerializer


class ProjectListSerializer(serializers.ModelSerializer):
    created_time = serializers.ReadOnlyField()

    class Meta(object):
        model = Project

        fields = ("id", "name", "created_time")


class ProjectDetailSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    created_time = serializers.ReadOnlyField()

    class Meta(object):
        model = Project

        fields = ("name", "description", "project_type", "author", "created_time")


class ContributorDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    project = ProjectDetailSerializer(many=True)
    created_time = serializers.ReadOnlyField()

    class Meta(object):
        model = Contributor

        fields = ("user", "project", "created_time")


class ContributorListSerializer(serializers.ModelSerializer):
    created_time = serializers.ReadOnlyField()

    class Meta(object):
        model = Contributor

        fields = ("id", "user", "project", "created_time")


class ContributorUserDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta(object):
        model = Contributor

        fields = ("user",)


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
    author = ContributorUserDetailSerializer()
    assigned_to = ContributorUserDetailSerializer()
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
    author = ContributorUserDetailSerializer()
    issue = IssueListSerializer()

    class Meta(object):
        model = Comment

        fields = ("id", "description", "author", "issue", "created_time")


class CommentListSerializer(serializers.ModelSerializer):
    created_time = serializers.ReadOnlyField()

    class Meta(object):
        model = Comment

        fields = ("id", "description", "author", "issue", "created_time")
