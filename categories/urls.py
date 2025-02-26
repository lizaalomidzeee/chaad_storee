from django.urls import path, include 
from rest_framework_nested import routers
from categories.views import CategoryViewSet, CategoryImageViewSet

router = routers.DefaultRouter()
router.register('categories', CategoryViewSet)

categories_router = routers.NestedSimpleRouter(router, 'categories', lookup='category')
categories_router.register('images', CategoryImageViewSet, basename='category-images')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(categories_router.urls)),
]