from django.urls import path 
from categories.views import CategoryDetailView, CategoryListView, CategoryImageViewSet




urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('categories/<int:category_id>/images/', CategoryImageViewSet.as_view({'get': 'list', 'post': 'create'}), name='category-images'),
]