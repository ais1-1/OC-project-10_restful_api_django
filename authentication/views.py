from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import CreateAPIView

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
