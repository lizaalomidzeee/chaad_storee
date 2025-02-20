from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from categories.serializers import CategorySerializer, CategoryDetailSerializer, CategoryImageSerializer
from categories.models import Category, CategoryImage
from rest_framework.viewsets import ModelViewSet


class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class= CategorySerializer
    permission_classes = [IsAuthenticated]

    


class CategoryDetailView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer
    permission_classes = [IsAuthenticated]



    

class CategoryImageViewSet(ModelViewSet):
    queryset = CategoryImage.objects.all()
    serializer_class = CategoryImageSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post']

    def get_queryset(self):
        return self.queryset.filter(category=self.kwargs['category_id'])
    


