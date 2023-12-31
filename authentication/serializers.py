from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from django.contrib.auth.hashers import make_password

from django.contrib.auth.password_validation import validate_password


User = get_user_model()


class UserSignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    age = serializers.IntegerField(required=True, min_value=15)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "age",
            "can_be_contacted",
            "can_data_be_shared",
            "password",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_password(self, value: str) -> str:
        if value is not None:
            return make_password(value)
        raise serializers.ValidationError("Password is empty")


class UserDetailSerializer(serializers.ModelSerializer):
    created_time = serializers.ReadOnlyField()

    class Meta(object):
        model = User

        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "age",
            "can_be_contacted",
            "can_data_be_shared",
            "created_time",
            "password",
        )

        extra_kwargs = {"password": {"write_only": True}}


class UserListSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User

        fields = (
            "id",
            "username",
        )
