from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet, RegisterViewSet


router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('register', RegisterViewSet, basename='register')


urlpatterns = [
    path('', include(router.urls))
]