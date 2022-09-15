from api.permissons import IsAdminOrReadOnly
from api.serializers import CategorySerializer, TitleSerializer
from rest_framework import permissions, viewsets
from rest_framework.pagination import PageNumberPagination
from reviews.models import Category, Genre, Title


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination
    
    def perform_create(self, serializer):
        serializer.save()
