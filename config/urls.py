from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include 

from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

schema_view = get_schema_view(
    openapi.Info(
        title = 'API for E-commerce platform',
        default_version='v1',
        description='E-commerce project for Mziuri'

    ),
    public=True,
    permission_classes=[permissions.AllowAny]

)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('products.urls')),
    path('', include('categories.urls')),
    path('', include('users.urls')),
    path("swagger/", schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
    path("redoc/", schema_view.with_ui('redoc', cache_timeout=0), name='redoc-ui'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
