from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import User
from .serializers import UserListSerializer, UserDetailSerializer


class UserViewset(ModelViewSet):
    serializer_class = UserListSerializer
    detail_serializer_class = UserDetailSerializer

    permission_classes = [IsAuthenticated]

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
        return super().get_serializer_class()
