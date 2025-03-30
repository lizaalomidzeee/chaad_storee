from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet, RegisterViewSet, ProfileViewSet, ResetPasswordViewSet


router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('register', RegisterViewSet, basename='register')
router.register('users', ProfileViewSet, basename='users_profile')
router.register('reset_password', ResetPasswordViewSet, basename='reset_password')

urlpatterns = [
    path('', include(router.urls))
]