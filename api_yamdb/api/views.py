from api.permissons import IsAdminOrReadOnly
from api.serializers import TitleSerializer
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from reviews.models import Title


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination
    
    def perform_create(self, serializer):
        serializer.save()
