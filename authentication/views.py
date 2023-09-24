from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status

from .models import User
from .serializers import UserListSerializer, UserDetailSerializer, UserSignupSerializer
from .permissions import IsOwnerOrReadOnly


class UserViewset(ModelViewSet):
    serializer_class = UserListSerializer
    detail_serializer_class = UserDetailSerializer

    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        # Show the users who gave permissions to share data
        if self.action == "retrieve":
            queryset = User.objects.filter(can_data_be_shared=True)
        else:
            print(self.action)
            queryset = User.objects.all()
        return queryset

    def get_serializer_class(self):
        if self.action == "retrieve" and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        if self.action == "update" and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


class UserSignupView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [
        AllowAny,
    ]
    serializer_class = UserSignupSerializer

    def post(self, request):
        # if email and username are already in use
        if User.objects.filter(email=request.data["email"]).exists():
            return Response(
                {"error": "Email already registered"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        elif User.objects.filter(username=request.data["username"]).exists():
            return Response(
                {"error": "Username already registered"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            serializer = UserSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
