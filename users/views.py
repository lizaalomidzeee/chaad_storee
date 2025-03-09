from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from users.serializers import UserSerializer, RegisterSerializer
User=get_user_model()


class UserViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer


class RegisterViewSet(CreateModelMixin, GenericViewSet):
    queryset=User.objects.all()
    serializer_class = RegisterSerializer



