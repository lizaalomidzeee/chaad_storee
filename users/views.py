from rest_framework import mixins, viewsets, permissions, response, status
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from users.serializers import UserSerializer, RegisterSerializer, ChangePasswordSerializer, PasswordResetSerializer
User=get_user_model()


class UserViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer


class RegisterViewSet(CreateModelMixin, GenericViewSet):
    queryset=User.objects.all()
    serializer_class = RegisterSerializer


class ProfileViewSet(GenericViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='change-password')
    def change_password(self, request):
        user = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({'old_password': 'Incorrect password'}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"detail": "Password changed successfully"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['delete'], url_path='delete')
    def delete_account(self, request):
        user = self.get_object()
        user.delete()
        return Response({"detail": "Account deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    





class ResetPasswordViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = PasswordResetSerializer

    def create(self, request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)


            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # reset_url = request.build_absolute_uri(
            #     reverse('password_reset_confirm', kwargs={"uidb64": uid, "token": token})
            # )

            reset_url = f"http://127.0.0.1:8000/reset_password_confirm/{uid}/{token}/"

            send_mail(
                'პაროლის აღდგენა',
                f"დააჭირეთ ლინკს რათა აღადგინოთ პაროლი {reset_url}",
                "noreply@example.com",
                [user.email],
                fail_silently=False
            )


            return response.Response({"message": 'წერილი წარმატებით არის გაგზავნილი'}, status=status.HTTP_200_OK)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


