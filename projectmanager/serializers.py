from rest_framework import serializers

from .models import Project, Contributor
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

        fields = ("user", "project", "created_time")
