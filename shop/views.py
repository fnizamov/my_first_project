from django.shortcuts import render, get_object_or_404
from requests import request
from rest_framework import mixins, status, filters
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
# from rest_framework.generics import ListAPIView
from django_filters import rest_framework as rest_filter

from .models import (
    Category, 
    Product, 
    Comment,
    Tag
)
from .serializers import (
    CommentSerializer,
    ProductSerializer,
    CategoryListSerializer,
    ProductCreateSerializer,
    TagSerializer
)

from .permissions import IsOwner


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer
    filter_backends = [
        filters.SearchFilter,
        rest_filter.DjangoFilterBackend,
        filters.OrderingFilter
    ]
    search_fields = ['name']
    filterset_fields = ['slug']
    ordering_fields = ['created']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductSerializer
        elif self.action == 'create':
            return ProductCreateSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        if self.action in ['create']:
            self.permission_classes = [IsAdminUser]
        if self.action in ['destroy', 'update', 'partial_update']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [
        filters.SearchFilter,
        rest_filter.DjangoFilterBackend,
        filters.OrderingFilter
    ]
    search_fields = ['name', 'user__username']
    filterset_fields = ['slug']
    ordering_fields = ['created']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductSerializer
        elif self.action == 'create':
            return ProductCreateSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        if self.action == 'comment' and self.request.method == 'DELETE':
            self.permission_classes = [IsOwner]
        if self.action in ['create', 'comment', 'set_rating', 'like']:
            self.permission_classes = [IsAuthenticated]
        if self.action in ['destroy', 'update', 'partial_update']:
            self.permission_classes = [IsOwner]
        return super().get_permissions()

    @action(detail=True, methods=['POST', 'DELETE'])
    def comment(self, request, pk=None):
        post = self.get_object()
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, post=post)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
                )

class CommentCreateDeleteView(
    mixins.DestroyModelMixin,
    GenericViewSet
    ):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwner]
    

class TagViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        if self.action == 'destroy':
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()
    
    # def product_list(request, category_slug=None):
    #     category = None
    #     categories = Category.objects.all()
    #     products = Product.objects.filter(available=True)
    #     if category_slug:
    #         category = get_object_or_404(Category, slug=category_slug)
    #         products = products.filter(category=category)
    #     return render(
    #         request,
    #         'shop/product/list.html',
    #         {'category': category,
    #         'categories': categories,
    #         'products': products}
    #     )

    # def product_detail(request, id, slug):
    #     product = get_object_or_404(
    #         Product,
    #         id=id,
    #         slug=slug,
    #         available=True)
    #     return render(
    #         request,
    #         'shop/product/detail.html',
    #         {'product': product}
    #     )
