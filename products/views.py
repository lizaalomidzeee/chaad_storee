from rest_framework.permissions import IsAuthenticated
from django.core.validators import ValidationError
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from products.pagination import ProductPagination
from products.filters import ProductFilter, ReviewFilter
from rest_framework.exceptions import PermissionDenied
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle, ScopedRateThrottle
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from products.permissions import IsObjectOwnerOrReadOnly
from rest_framework.decorators import action
from products.models import (
    CartItem,
    Product,
    Review,
    FavoriteProduct,
    Cart, ProductTag, ProductImage
)
from products.serializers import (
    CartItemSerializer,
    ProductSerializer,
    ReviewSerializer,
    Favoriteproductserializer,
    CartSerializer,
    ProductTagSerializer,
    ProductImageSerializer
    )


class ProductViewSet(ModelViewSet):

    queryset = Product.objects.all().prefetch_related('reviews', 'tags')
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['price', 'categories']
    filterset_class = ProductFilter
    # pagination_class = ProductPagination
    search_fields = ['name', 'desctiption']
    throttle_classes = [UserRateThrottle]

    def get_serialized_data(self):
        from django.core.cache import cache
        cache_key = 'products_list'
        cached_data = cache.get(cache_key)

        if cached_data:
            return cached_data
        
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        cache.set('products_list', serializer.data, 60*10)
        return serializer.data


    def list(self, request, *args, **kwargs):
        import time
        start = time.time()
        data = self.get_serialized_data()
        end = time.time()
        print(end-start)
        return Response(data)
    
    
    # @action(detail=False, methods=['get'], url_path='my_products')
    # def my_products(self, request):
    #     user_products = Product.objects.filter(user=request.user)
    #     serializer = self.get_serializer(user_products, many=True)
    #     return Response(serializer.data)


    
    
    
class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsObjectOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['rating']
    filterset_class = ReviewFilter

    def get_queryset(self):
        return self.queryset.filter(product_id=self.kwargs['product_pk'])
    
    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("You Cant delete this review")
        instance.delete()
        
    def perform_update(self, serializer):
        instance = self.get_object()
        if instance.user != self.request.user:
            raise PermissionDenied("You Cant change this review")
        serializer.save()


    

class FavoriteProductViewSet(ModelViewSet):
    queryset = FavoriteProduct.objects.all()
    serializer_class = Favoriteproductserializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'delete']
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'likes'

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        return queryset
    

    

class CartViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated] 

    def get_queryset(self, *args, **kwargs):
        queryset = self.queryset.filter(user=self.request.user)
        return queryset
    

    


class ProductTagListView(ListModelMixin, GenericViewSet):
    queryset = ProductTag.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    



class ProductImageViewSet(ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queyset(self):
        self.queryset.filter(product_id=self.kwargs['product_pk'])

    def create(self, request, *args, **kwargs):
        try:
            super().create(request, *args, **kwargs)
        except ValidationError as e:
            return Response ({f"error":"{e}"}, status=status.HTTP_400_BAD_REQUEST)



class CartItemViewSet(ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]
    
    
    def get_queryset(self):
        return self.queryset.filter(cart__user=self.request.user)
    
    
    def perform_destroy(self, instance):
        if instance.cart.user != self.request.user:
            raise PermissionDenied("You do not have permission to delete this review")
        instance.delete()
        
        
    def perform_update(self, serializer):
        isinstance = self.get_object()
        if instance.cart.user != self.request.user:
            raise PermissionDenied("You do not have permission to update this item")
        serializer.save()
    

    
    


