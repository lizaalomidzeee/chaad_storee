from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet, RegisterViewSet, ProfileViewSet, ResetPasswordViewSet, ResetPasswordConfirmViewSet


router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('register', RegisterViewSet, basename='register')
router.register('users', ProfileViewSet, basename='users_profile')
router.register('reset_password', ResetPasswordViewSet, basename='reset_password')

urlpatterns = [
    path("password_reset_confirm/<uidb64>/<token>", ResetPasswordConfirmViewSet.as_view({"post":"create"}), name="password_reset_confirm"),
    path('', include(router.urls))
]